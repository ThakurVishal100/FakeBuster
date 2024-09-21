from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
import PIL
from tkinter import messagebox
import mysql.connector #pip install mqsql-connector-python (ppower shell) 
import cv2
import os
import csv
from tkinter import filedialog

mydata=[]
class Attendance:
   def __init__(self,root):
       self.root=root
       self.root.geometry("1530x790+0+0")
       self.root.title("Face Attendence System")

        #=================variblares============
       self.var_atten_id=StringVar()
       self.var_atten_roll=StringVar()
       self.var_atten_name=StringVar()
       self.var_atten_dep=StringVar()
       self.var_atten_time=StringVar()
       self.var_atten_date=StringVar()
       self.var_atten_attendance=StringVar()

        #    image 1   
       img1=Image.open(r"D:\0-done\face recognization system\images.jpeg")
       img1=img1.resize((800,200),Image.ANTIALIAS)
       self.photoimg1=ImageTk.PhotoImage(img1)

       f_lbl=Label(self.root,image=self.photoimg1)
       f_lbl.place(x=0,y=0,width=800,height=200)


     #    image 2
       img2=Image.open(r"D:\0-done\face recognization system\download.jpeg")
       img2=img2.resize((800,200),Image.ANTIALIAS)
       self.photoimg2=ImageTk.PhotoImage(img2)

       f_lbl=Label(self.root,image=self.photoimg2)
       f_lbl.place(x=800,y=0,width=800,height=200) 

       title_lbl=Label(text="ATTENDANCE MANAGEMENT SYSTEM",font=("Calibri",35,"bold"),bg="white",fg="red" )
       title_lbl.place(x=0,y=200,width=1530,height=45)

       main_frame=Frame(bd=2)
       main_frame.place(x=10,y=250,width=1500,height=600)
       #left label frame
       Left_frame=LabelFrame(main_frame,bd=2,relief=RIDGE,text="Student Details",font=("times new roman",12,"bold"))
       Left_frame.place(x=10,y=10,width=770,height=550)
       img_left=Image.open(r"D:\0-done\face recognization system\student2.jpeg")
       img_left=img_left.resize((720,130),Image.ANTIALIAS)
       self.photoimg_left=ImageTk.PhotoImage(img_left)
       
       
       f_lbl=Label(Left_frame,image=self.photoimg_left)
       f_lbl.place(x=5,y=0,width=720,height=130)

       left_inside_frame=Frame(Left_frame,bd=2,relief=RIDGE,bg="white")
       left_inside_frame.place(x=0,y=135,width=750,height=370)

      #  ======= entry====
       #attendanceID
       attendanceID_label=Label(left_inside_frame,text="ATTENDANCE ID",bg="white",font="comicsansns 12 bold")
       attendanceID_label.grid(row=0,column=0,padx=10,pady=5,sticky=W)

       attendanceID_entry=ttk.Entry(left_inside_frame,width=20,textvariable=self.var_atten_id,font="comicsansns 12 bold")
       attendanceID_entry.grid(row=0,column=1,padx=10,pady=5,sticky=W)

       #Roll
       rolllabel=Label(left_inside_frame,text="Roll:",bg="white",font="comicsansns 12 bold")
       rolllabel.grid(row=0,column=2,padx=4,pady=8)

       atten_roll=ttk.Entry(left_inside_frame,width=22,textvariable=self.var_atten_roll,font="comicsansns 12 bold")
       atten_roll.grid(row=0,column=3,pady=8)

       #name
       name_label=Label(left_inside_frame,text="Name:",bg="white",font="comicsansns 12 bold")
       name_label.grid(row=1,column=0)

       atten_name=ttk.Entry(left_inside_frame,width=22,textvariable=self.var_atten_name,font="comicsansns 12 bold")
       atten_name.grid(row=1,column=1,pady=8)
       #Department
       dep_label=Label(left_inside_frame,text="Department:",bg="white",font="comicsansns 12 bold")
       dep_label.grid(row=1,column=2)

       atten_dep=ttk.Entry(left_inside_frame,width=22,textvariable=self.var_atten_dep,font="comicsansns 12 bold")
       atten_dep.grid(row=1,column=3,pady=8)
       #Time
       time_label=Label(left_inside_frame,text="Time:",bg="white",font="comicsansns 12 bold")
       time_label.grid(row=2,column=0)

       atten_time=ttk.Entry(left_inside_frame,width=22,textvariable=self.var_atten_time,font="comicsansns 12 bold")
       atten_time.grid(row=2,column=1,pady=8)
       #Date
       date_label=Label(left_inside_frame,text="Date:",bg="white",font="comicsansns 12 bold")
       date_label.grid(row=2,column=2)

       atten_date=ttk.Entry(left_inside_frame,width=22,textvariable=self.var_atten_date,font="comicsansns 12 bold")
       atten_date.grid(row=2,column=3,pady=8)
       #attendance
       attendance_label=Label(left_inside_frame,text="Attendance status",bg="white",font="comicsansns 12 bold")
       attendance_label.grid(row=3,column=0)

       self.atten_status=ttk.Combobox(left_inside_frame,textvariable=self.var_atten_attendance,width=20,font="comicsansns 12 bold",state="readonly")
       self.atten_status["values"]=("Status","Present","Absent")
       self.atten_status.grid(row=3,column=1,pady=8)
       self.atten_status.current(0)

       #button framd1
       button1=Frame(left_inside_frame,bd=2,relief=RIDGE)
       button1.place(x=0,y=300,width =715,height=35)
      
       import_button=Button(button1,text="Import csv",width=17,command=self.importCsv,font=("Times new roman",13,"bold"),bg="blue",fg="white")
       import_button.grid(row=0,column=0)
      
       export_button=Button(button1,text="Export csv ",width=17,command=self.exportCsv,font=("Times new roman",13,"bold"),bg="blue",fg="white")
       export_button.grid(row=0,column=1)
      
       update_button=Button(button1,text="Update",width=17,font=("Times new roman",13,"bold"),bg="blue",fg="white")
       update_button.grid(row=0,column=2)

       reset_button=Button(button1,text="Reset",width=17,command=self.reset_data,font=("Times new roman",13,"bold"),bg="blue",fg="white")
       reset_button.grid(row=0,column=3)
       

       

 
        #right label frame
       right_frame=LabelFrame(main_frame,bd=2,relief=RIDGE,text="Student Details",font=("times new roman",12,"bold"))
       right_frame.place(x=750,y=10,width=740,height=550)

       table_frame=Frame(right_frame,bd=2,relief=RIDGE,bg="white")
       table_frame.place(x=5,y=5,width =720,height=450)

       scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
       scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)
       
       self.AttendanceReporttable=ttk.Treeview(table_frame,column=("id","roll","name","department","time","date","attendance"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
       
       scroll_x.pack(side=BOTTOM,fill=X)
       scroll_y.pack(side=RIGHT,fill=Y)
       scroll_x.config(command=self.AttendanceReporttable.xview)
       scroll_y.config(command=self.AttendanceReporttable.yview)

       self.AttendanceReporttable.heading("id",text="Attendance ID")
       self.AttendanceReporttable.heading("roll",text="ROLL")
       self.AttendanceReporttable.heading("name",text="NAME")
       self.AttendanceReporttable.heading("department",text="Department")
       self.AttendanceReporttable.heading("time",text="TIME")
       self.AttendanceReporttable.heading("date",text="Date")
       self.AttendanceReporttable.heading("attendance",text="Attendence")
       self.AttendanceReporttable["show"]="headings"

       self.AttendanceReporttable.column("id",width=100)
       self.AttendanceReporttable.column("roll",width=100)
       self.AttendanceReporttable.column("name",width=100)
       self.AttendanceReporttable.column("department",width=100)
       self.AttendanceReporttable.column("time",width=100)
       self.AttendanceReporttable.column("date",width=100)
       self.AttendanceReporttable.column("attendance",width=100)

       

       self.AttendanceReporttable.pack(fill=BOTH,expand=1)
      
   def fetchdata(self,rows):
           self.AttendanceReporttable.delete(*self.AttendanceReporttable.get_children())
           for i in rows:   
            self.AttendanceReporttable.insert("",END,values=i)
   def importCsv(self):
          global mydata
          mydata.clear()
          fln=filedialog.askopenfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV file","*.csv"),("All file","*.*")),parent=self.root)
          with open(fln) as myfile:
             csvread=csv.reader(myfile,delimiter=",")
             for i in csvread:
                mydata.append(i)
             self.fetchdata(mydata)

  #  ======= export funcition====/
   def exportCsv(self):   
      try:
          if len(mydata)<1:
              messagebox.showerror("no data","no data found to export",parent=self.root)
              return False
          fln=filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV file","*.csv"),("All file","*.*")),parent=self.root)
          with open(fln,mode="w",newline="") as myfile:
              exp_write=csv.writer(myfile,delimiter=",")
              for i in mydata:
                  exp_write.writerow(i)
                  messagebox.showinfo("data export","your data exported to"+os.path.basename(fln)+"succesfully")
      except Exception as es:
                messagebox.showerror("Error",f"Due to :{str(es)}",parent=self.root)

   def get_cursor(self,event=""):
    cursor_row=self.AttendanceReporttable.focus()
    content=self.AttendanceReporttable.item(cursor_row)
    rows=content['values']
    self.var_atten_id.set(rows[0]),
    self.var_atten_roll.set(rows[1]),
    self.var_atten_name.set(rows[2]),
    self.var_atten_dep.set(rows[3]),
    self.var_atten_time.set(rows[4]),
    self.var_atten_date.set(rows[5]),
    self.var_atten_attendance.set(rows[6])

    self.AttendanceReporttable.bind("<ButtonRelease>",self.get_cursor)
   
   def reset_data(self):

    self.var_atten_id.set(""),
    self.var_atten_roll.set(""),
    self.var_atten_name.set(""),
    self.var_atten_dep.set(""),
    self.var_atten_time.set(""),
    self.var_atten_date.set(""),
    self.var_atten_attendance.set("")
    
    
    

          
            
          
                  
             
                       





if __name__ == "__main__":
    root=Tk()
    obj=Attendance(root)
    root.mainloop()  
