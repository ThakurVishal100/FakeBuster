from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import torch
import torch.nn.functional as F
from facenet_pytorch import MTCNN, InceptionResnetV1
import numpy as np
import cv2
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
from pytorch_grad_cam.utils.image import show_cam_on_image
import warnings

warnings.filterwarnings("ignore")

# Set device based on availability of CUDA
DEVICE = 'cuda:0' if torch.cuda.is_available() else 'cpu'

# Initialize MTCNN for face detection
mtcnn = MTCNN(select_largest=False, post_process=False, device=DEVICE).to(DEVICE).eval()

# Initialize InceptionResnetV1 for face recognition
model = InceptionResnetV1(pretrained="vggface2", classify=True, num_classes=1, device=DEVICE)

# Load pre-trained model checkpoint
checkpoint = torch.load("resnetinceptionv1_epoch_32.pth", map_location=torch.device('cpu'))
model.load_state_dict(checkpoint['model_state_dict'])
model.to(DEVICE)
model.eval()

def predict(input_image: Image.Image):
    """Predict the label of the input_image"""
    face = mtcnn(input_image)
    if face is None:
        raise Exception('No face detected')
    face = face.unsqueeze(0)  # add the batch dimension
    face = F.interpolate(face, size=(256, 256), mode='bilinear', align_corners=False)
    
    # Convert the face into a numpy array for visualization
    prev_face = face.squeeze(0).permute(1, 2, 0).cpu().detach().int().numpy()
    prev_face = prev_face.astype('uint8')

    face = face.to(DEVICE)
    face = face.to(torch.float32)
    face = face / 255.0
    face_image_to_plot = face.squeeze(0).permute(1, 2, 0).cpu().detach().int().numpy()

    target_layers = [model.block8.branch1[-1]]
    use_cuda = True if torch.cuda.is_available() else False
    cam = GradCAM(model=model, target_layers=target_layers, use_cuda=use_cuda)
    targets = [ClassifierOutputTarget(0)]

    grayscale_cam = cam(input_tensor=face, targets=targets, eigen_smooth=True)
    grayscale_cam = grayscale_cam[0, :]
    visualization = show_cam_on_image(face_image_to_plot, grayscale_cam, use_rgb=True)
    face_with_mask = cv2.addWeighted(prev_face, 1, visualization, 0.5, 0)

    with torch.no_grad():
        output = torch.sigmoid(model(face).squeeze(0))
        prediction = "real" if output.item() < 0.5 else "fake"
        
        real_prediction = 1 - output.item()
        fake_prediction = output.item()
        
        confidences = {
            'real': real_prediction,
            'fake': fake_prediction
        }
    return confidences, face_with_mask


class FaceRecognitionSystem:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("DEEP FAKE DETECTION SOFTWARE")

        # Image 1
        img1 = Image.open(r"D:\matrix\images/b2.jpg")
        img1 = img1.resize((500, 130), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl = Label(self.root, image=self.photoimg1)
        f_lbl.place(x=0, y=0, width=500, height=130)

        # Image 2
        img2 = Image.open(r"D:\matrix\images/facce2.jpg")
        img2 = img2.resize((500, 130), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl = Label(self.root, image=self.photoimg2)
        f_lbl.place(x=500, y=0, width=500, height=130)

        # Image 3
        img3 = Image.open(r"D:\matrix\images/face 2.jpg")
        img3 = img3.resize((500, 130), Image.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        f_lbl = Label(self.root, image=self.photoimg3)
        f_lbl.place(x=1000, y=0, width=550, height=130)

        # Background image
        img4 = Image.open(r"D:\matrix\images/mainbg.png")
        img4 = img4.resize((1530, 710), Image.LANCZOS)
        self.photoimg4 = ImageTk.PhotoImage(img4)

        bg_image = Label(self.root, image=self.photoimg4)
        bg_image.place(x=0, y=130, width=1530, height=710)

        # Title
        title_lbl = Label(bg_image, text="FakeBuster", font=("Calibri", 35, "bold"), bg="white", fg="red")
        title_lbl.place(x=0, y=0, width=1530, height=45)

        # Upload Button
        self.upload_btn = Button(bg_image, text="Upload Image", command=self.upload_image, font=("Arial", 15, "bold"), bg="blue", fg="white")
        self.upload_btn.place(x=700, y=100, width=200, height=50)

        # Label for displaying results
        self.result_label = Label(bg_image, text="", font=("Arial", 20, "bold"), bg="white", fg="green")
        self.result_label.place(x=550, y=180, width=500, height=50)

        # Area for displaying the processed image (with CAM heatmap)
        self.image_area = Label(bg_image, bg="white")
        self.image_area.place(x=600, y=250, width=400, height=300)

    def upload_image(self):
        # Open file dialog to select an image
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
        if not file_path:
            return

        # Load the image
        img = Image.open(file_path)

        # Run the face recognition prediction
        try:
            confidences, face_with_mask = predict(img)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        
        # Display the results on the UI
        prediction_text = f"Real: {confidences['real']:.2f} |  Fake: {confidences['fake']:.2f}"
        self.result_label.config(text=prediction_text)

        # Convert the output image (face_with_mask) to ImageTk format for display
        img_with_mask = Image.fromarray(cv2.cvtColor(face_with_mask, cv2.COLOR_BGR2RGB))
        img_with_mask = img_with_mask.resize((500, 400), Image.LANCZOS)
        self.photo_masked_img = ImageTk.PhotoImage(img_with_mask)

        self.image_area.config(image=self.photo_masked_img)

    def exit(self):
        self.exit_confirm = messagebox.askyesno("Face Recognition", "Are you sure you want to exit?")
        if self.exit_confirm > 0:
            self.root.destroy()
        else:
            return

if __name__ == "__main__":
    root = Tk()
    obj = FaceRecognitionSystem(root)
    root.mainloop()
