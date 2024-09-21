from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk 
import tkinter
import PIL
import os
from time import strftime
from datetime import datetime



class face_recognization_system: 
   def __init__(self,root):
       self.root=root
       self.root.geometry("1530x790+0+0")
       self.root.title("Face Recognization System")

    #    image 1   
       img1=Image.open(r"D:\matrix\images/b2.jpg")
       img1=img1.resize((500,130),Image.LANCZOS)
       self.photoimg1=ImageTk.PhotoImage(img1)

       f_lbl=Label(self.root,image=self.photoimg1)
       f_lbl.place(x=0,y=0,width=500,height=130)


    #    image 2
       img2=Image.open(r"D:\matrix\images/facce2.jpg")
       img2=img2.resize((500,130),Image.LANCZOS)
       self.photoimg2=ImageTk.PhotoImage(img2)

       f_lbl=Label(self.root,image=self.photoimg2)
       f_lbl.place(x=500,y=0,width=500,height=130)


    #    image 3
       img3=Image.open(r"D:\matrix\images/face 2.jpg")
       img3=img3.resize((500,130),Image.LANCZOS)
       self.photoimg3=ImageTk.PhotoImage(img3)

       f_lbl=Label(self.root,image=self.photoimg3)
       f_lbl.place(x=1000,y=0,width=550,height=130)

       # image 4 (bg image)
       img4=Image.open(r"D:\matrix\images/mainbg.png")
       img4=img4.resize((1530,710),Image.LANCZOS)
       self.photoimg4=ImageTk.PhotoImage(img4)

       bg_image=Label(self.root,image=self.photoimg4)
       bg_image.place(x=0,y=130,width=1530,height=710)
       


       title_lbl=Label(bg_image,text="FACE RECOGNIZATION SYSTEM SOFTWARE",font=("Calibri",35,"bold"),bg="white",fg="red" )
       title_lbl.place(x=0,y=0,width=1530,height=45)
    
  
    # image call function ====
   def open_img(self):
      os.startfile("images data ")
   def exit(self):
      self.exit=tkinter.messagebox.askyesno("face recognization","Are you sure to exit ?",parent=self.root)
      if self.exit>0:
         self.root.destroy()
      else:
         return      
     #==================== student page call function =================
  


   
   # def attendence(self):
   #    self.new_window=Toplevel(self.root)
   #    self.app=Attendance(self.new_window)   
    



if __name__ == "__main__":
    root=Tk()
    obj=face_recognization_system(root)
    root.mainloop()

