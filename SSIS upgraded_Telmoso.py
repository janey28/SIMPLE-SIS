#Author: Jane Ann Telmoso
import tkinter as tk
from tkinter import font as tkfont
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter.messagebox
import sqlite3

class SSIS(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)
        self.frames = {}
        
        for F in (Student, Dashboard, Course):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(Dashboard)
        
    def show_frame(self, page_number):
        frame = self.frames[page_number]
        frame.tkraise()
    

class Dashboard(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        
#============================ DESIGN ==============================#
        #========== FRAME =============#
        LeftFrame = Frame(self, width=250, height=800, padx=2, bg="#a39193", relief=RIDGE)
        LeftFrame.pack(side=LEFT)
        topFrame = Frame(self, width=1350, height=30, padx=2, bg="#66545e", relief=RIDGE)
        topFrame.pack(side=TOP)
        
        
        self.title = Label(LeftFrame, font=("rockwell", 55), bg="#a39193",text="SIS", fg="snow")
        self.title.place(x=40,y=10) 
         
        totalenrolledstudents = StringVar()
        totalenrolledcourses = StringVar()
        ## Window Buttons
        
        button1 = tk.Button(self, text="DASHBOARD",font=("rockwell", 18),bd=0,
                            bg="#a39193",
                            fg="snow",
                            command=lambda: controller.show_frame(Dashboard))
        button1.place(x=40,y=160)
        button1.config(cursor= "hand2")

        button2 = tk.Button(self, text="STUDENTS",font=("rockwell",18),bd=0,
                            bg="#a39193",
                            fg="snow",
                            command=lambda: controller.show_frame(Student))
        button2.place(x=40,y=260)
        button2.config(cursor= "hand2")
        
        button3 = tk.Button(self, text="COURSE",font=("rockwell",18),bd=0,
                            bg="#a39193",
                            fg="snow",
                            command=lambda: controller.show_frame(Course))
        button3.place(x=40,y=360)
        button3.config(cursor= "hand2")
        
        def connect():
            conn = sqlite3.connect("SIS.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("CREATE TABLE IF NOT EXISTS students (StudentIDNumber TEXT PRIMARY KEY, StudentLastName TEXT,\
                    StudentFirstName TEXT, StudentMiddleInitial TEXT, CourseCode TEXT, StudentYearLevel TEXT, StudentGender TEXT,\
                    FOREIGN KEY(CourseCode) REFERENCES courses(CourseCode) \
                    ON UPDATE CASCADE)") 
            conn.commit() 
            conn.close()
            
        def displayData():
            tree.delete(*tree.get_children())
            conn = sqlite3.connect("SIS.db")
            cur = conn.cursor()
            cur.execute("PRAGMA foreign_keys = ON")
            cur.execute("SELECT * FROM students")
            rows = cur.fetchall()
            for row in rows:
                tree.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()
            
        def enrolledstudents():
            conn = sqlite3.connect("SIS.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM students")
            rows = cur.fetchall()
            totalenrolledstudents.set(len(rows))
            self.totalenrolled = Label(self, font=("rockwell", 40, "bold"),textvariable = totalenrolledstudents, bg ="#aa6f73", fg = "snow")
            self.totalenrolled.place(x=430,y=170)
            self.after(1000,enrolledstudents)
            conn.commit()            
            conn.close()

        def enrolledcourses():
            conn = sqlite3.connect("SIS.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            totalenrolledcourses.set(len(rows))
            self.totalcourses = Label(self, font=("rockwell", 40, "bold"),textvariable = totalenrolledcourses, bg ="#aa6f73", fg = "snow")
            self.totalcourses.place(x=430,y=360)
            self.after(1000,enrolledcourses)
            conn.commit()            
            conn.close()

        self.label=Label(self, pady=1,bd=1,font=('helvetica',12,'bold'), padx=24, width=20,height=8, text='\nEnrolled Students', bg="#aa6f73", fg="snow", anchor = N)
        self.label.place(x=340,y=100)

        self.label=Label(self, pady=1,bd=1,font=('helvetica',12,'bold'), padx=24, width=20,height=8, text='\nAvailable Courses', bg="#aa6f73", fg="snow", anchor = N)
        self.label.place(x=340,y=300)
      
        scroll_y=Scrollbar(self, orient=VERTICAL)
    
        tree = ttk.Treeview(self, height=20, columns=("ID Number", "Last Name", "First Name", "Middle Initial", "Course", "Year Level", "Gender"), yscrollcommand=scroll_y.set)
    
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.place(x=1328,y=79,height=388)
        
        tree.heading("ID Number", text="ID Number")
        tree.heading("Last Name", text="Last Name")
        tree.heading("First Name", text="First Name")
        tree.heading("Middle Initial", text="Middle Initial")   
        tree.heading("Course", text="Course")
        tree.heading("Year Level", text="Year Level")
        tree.heading("Gender", text="Gender")
        tree['show'] = 'headings'
    
        tree.column("ID Number", width=90)
        tree.column("Last Name", width=100)
        tree.column("First Name", width=130)
        tree.column("Middle Initial", width=80)
        tree.column("Course", width=90)
        tree.column("Year Level", width=70)
        tree.column("Gender", width=60)
        scroll_y.config(command=tree.yview)
        tree.pack(fill=BOTH,expand=1)
        tree.place(x=680, y=79)
        
        
        
        connect()
        displayData()
        enrolledstudents()
        enrolledcourses()


class Course(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.controller.title("Student Information System")
        
        apptitle = tk.Label(self, text="SIS", font=("rockwell",15,"bold"),bd=0,
                            bg="#66545e",
                            fg="snow",)
        apptitle.place(x=20,y=70)
        
        
        CourseCode = StringVar()
        CourseName = StringVar()
        searchbar = StringVar()
        
        def connectCourse():
            conn = sqlite3.connect("SIS.db")
            cur = conn.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS courses (CourseCode TEXT PRIMARY KEY, CourseName TEXT)") 
            conn.commit() 
            conn.close()


        #======= ADD COURSE ========#   
        def addCourse():
            if CourseCode.get() == "" or CourseName.get() == "":
                tkinter.messagebox.showinfo("Student Information System", "Please fill in the box")
            else:
                conn = sqlite3.connect("SIS.db")
                c = conn.cursor()
                c.execute("INSERT INTO courses(CourseCode,CourseName) VALUES (?,?)",\
                          (CourseCode.get(),CourseName.get()))    
                conn.commit()           
                conn.close()
                CourseCode.set('')
                CourseName.set('') 
                tkinter.messagebox.showinfo("Student Information System", "Course Recorded Successfully")
                displayCourse()

         #======= DISPLAY COURSE ========#     
        def displayCourse():
            tree.delete(*tree.get_children())
            conn = sqlite3.connect("SIS.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM courses")
            rows = cur.fetchall()
            for row in rows:
                tree.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()

        #======= UPDATE COURSE ========#
        def updateCourse():
            for selected in  tree.selection():
                conn = sqlite3.connect("SIS.db")
                cur = conn.cursor()
                cur.execute("UPDATE courses SET CourseCode=?, CourseName=? WHERE CourseCode=?", \
                            (CourseCode.get(),CourseName.get(),  tree.set(selected, '#1')))                       
                conn.commit()
                tkinter.messagebox.showinfo("Student Information System", "Course Updated Successfully")
                displayCourse()
                conn.close()

        #======= EDIT COURSE ========#        
        def editCourse():
            x =  tree.focus()
            if x == "":
                tkinter.messagebox.showerror("Student Information System", "Please select a student record from the table")
                return
            values =  tree.item(x, "values")
            CourseCode.set(values[0])
            CourseName.set(values[1])

        #======= DELETE COURSE ========#           
        def deleteCourse(): 
            messageDelete = tkinter.messagebox.askyesno("Student Information System", "Are you sure to delete Course Record?")
            try:
                if messageDelete > 0:   
                   con = sqlite3.connect("SIS.db")
                   cur = con.cursor()
                   x =  tree.selection()[0]
                   coursecode = tree.item(x)["values"][0]
                   cur.execute("PRAGMA foreign_keys = ON")
                   cur.execute("DELETE FROM courses WHERE CourseCode = ?",(coursecode,))                   
                   con.commit()
                   tree.delete(x)
                   tkinter.messagebox.showinfo("Student Information System", "Course is Deleted Successfully")
                   displayCourse()
                   con.close()          
            except:
                tkinter.messagebox.showerror("Student Information System", "Students are still enrolled in this course.")

        #======= SEARCH COURSE BY COURSE CODE ========#        
        def searchCourse():
            CourseCode = searchbar.get()                
            con = sqlite3.connect("SIS.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM courses WHERE CourseCode = ?",(CourseCode,))
            con.commit()
            tree.delete(* tree.get_children())
            rows = cur.fetchall()
            for row in rows:
                 tree.insert("", tk.END, text=row[0], values=row[0:])
            con.close()

 
        def Refresh():
            displayCourse()
        
        def clear():
            CourseCode.set('')
            CourseName.set('') 
            
#============================ DESIGN ==============================#
        #===== FRAME =======#
        LeftFrame = Frame(self, width=250, height=800, padx=2, bg="#a39193", relief=RIDGE)
        LeftFrame.pack(side=LEFT)
        topFrame = Frame(self, width=1350, height=30, padx=2, bg="#66545e", relief=RIDGE)
        topFrame.pack(side=TOP)
        
        #===== LABELS & ENTRIES =======#
        
        self.lblCourseCode = Label(self, font=('helvetica',12,'bold'), text="Course Code", bd=7 , anchor=W)
        self.lblCourseCode.place(x=275,y=75)
        self.txtCourseCode = Entry(self, font=('helvetica',12,'bold'), width=30, justify='left', textvariable = CourseCode)
        self.txtCourseCode.place(x=390,y=80)
    
        self.lblCourseName = Label(self, font=('helvetica',12,'bold'), text="Course Name", bd=7, anchor=W)
        self.lblCourseName.place(x=275,y=105)
        self.txtCourseName = Entry(self, font=('helvetica',12,'bold'), width=30, justify='left', textvariable = CourseName)
        self.txtCourseName.place(x=390,y=110)
            
        self.searchbar = Entry(self, font=('helvetica',12,'bold'), textvariable = searchbar, width = 25)
        self.searchbar.place(x=680,y=45)
        self.searchbar.insert(0,'Enter course code')
            
        self.title = Label(LeftFrame, font=("rockwell", 55), bg="#a39193",text="SIS", fg="snow")
        self.title.place(x=40,y=10)    
        
        #===== BUTTONS =======#
        
        self.btnAddNew=Button(self, pady=1,bd=4,font=('helvetica',12,'bold'), padx=24, width=10, text='Add Course', bg="#7f5539", fg="snow", command=addCourse)
        self.btnAddNew.place(x=280,y=320)
            
        self.btnClear=Button(self, pady=1,bd=4,font=('helvetica',12,'bold'), padx=24, width=10, text='Clear Fields', bg="#7f5539", fg="snow",command=clear)
        self.btnClear.place(x=500,y=320)
                
        self.btnUpdate=Button(self, pady=1,bd=4,font=('helvetica',12,'bold'), padx=24, width=10, text='Update Course', bg="#7f5539", fg="snow",command=updateCourse)
        self.btnUpdate.place(x=500,y=380)

        self.btnEdit=Button(self, pady=1,bd=4,font=('helvetica',12,'bold'), padx=24, width=10, text='Edit Course', bg="#7f5539", fg="snow",command = editCourse)
        self.btnEdit.place(x=280,y=380)

        self.btnDelete=Button(self, pady=1,bd=4,font=('helvetica',12,'bold'), padx=24, width=10, text='Delete Course',bg="#7f5539", fg="snow",command = deleteCourse)
        self.btnDelete.place(x=380,y=440)

        self.btnSearch=Button(self,bd=1,font=('helvetica',12,'bold'), width=10, text='Search', bg="#7f5539", fg="snow",command = searchCourse)
        self.btnSearch.place(x=920,y=41)
        
        self.btnShowAll=Button(self,bd=1,font=('helvetica',12,'bold'), width=10, text='Show All', bg="#7f5539", fg="snow", command = displayCourse)
        self.btnShowAll.place(x=1100,y=41)
        
        #====== Window Buttons =======#
        
        button1 = tk.Button(self, text="DASHBOARD",font=("rockwell",18),bd=0,
                            bg="#a39193",
                            fg="snow",
                            command=lambda: controller.show_frame(Dashboard))
        button1.place(x=40,y=160)
        button1.config(cursor= "hand2")
        
        button2 = tk.Button(self, text="STUDENTS",font=("rockwell",18),bd=0,
                            bg="#a39193",
                            fg="snow",
                            command=lambda: controller.show_frame(Student))
        button2.place(x=40,y=260)
        button2.config(cursor= "hand2")
        
        button3 = tk.Button(self, text="COURSE",font=("rockwell",18),bd=0,
                            bg="#a39193",
                            fg="snow",
                            command=lambda: controller.show_frame(Course))
        button3.place(x=40,y=360)
        button3.config(cursor= "hand2")
        
        scroll_y=Scrollbar(self, orient=VERTICAL)
        #scroll_y.grid(row=1, column=1, sticky='ns')
    
        tree = ttk.Treeview(self, height=20, columns=("Course Code", "Course Name"), yscrollcommand=scroll_y.set)
    
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.place(x=1328,y=79,height=388)
        
        tree.heading("Course Code", text="Course Code")
        tree.heading("Course Name", text="Course Name")

        tree['show'] = 'headings'
    
        tree.column("Course Code", width=200)
        tree.column("Course Name", width=440)
        scroll_y.config(command=tree.yview)
        tree.pack(fill=BOTH,expand=1)
        tree.place(x=680, y=79)
        
        connectCourse()
        displayCourse()


class Student(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self.controller = controller
        self.controller.title("Student Information System")

        StudentFirstName = StringVar()
        StudentMiddleInitial = StringVar()
        StudentLastName = StringVar()
        StudentIDNumber = StringVar()
        StudentYearLevel = StringVar()
        StudentGender = StringVar()
        CourseCode = StringVar()
        searchbar = StringVar()
        

        
        #====== ADD NEW STUDENT ========#
        
        def addStudent(): 
            if StudentIDNumber.get() == "" or StudentLastName.get() == "" or StudentFirstName.get() == "" \
                or CourseCode.get() == "" or StudentYearLevel.get() == "" or StudentGender.get() == "": 
                tkinter.messagebox.showinfo("Student Information System", "Please fill in the box.")
            else:  
                studentID = StudentIDNumber.get()
                studentID_list = []
                for i in studentID:
                    studentID_list.append(i)
                a = studentID.split("-")
                if len(a[0]) == 4:        
                    if "-" in studentID_list:
                        if len(a[1]) == 1:
                            tkinter.messagebox.showerror("Student Information System", "Invalid ID Number")
                        elif len(a[1]) ==2:
                            tkinter.messagebox.showerror("Student Information System", "Invalid ID Number")
                        elif len(a[1]) ==3:
                            tkinter.messagebox.showerror("Student Information System", "Invalid ID Number")
                        else:
                            x = studentID.split("-")
                            y = x[0]
                            n = x[1]
                            if y.isdigit()==False or n.isdigit()==False:
                                try:
                                    tkinter.messagebox.showerror("Student Information System", "Invalid ID")
                                except:
                                    pass
                            elif y==" " or n==" ":
                                try:
                                    tkinter.messagebox.showerror("Student Information System", "Invalid ID")
                                except:
                                    pass
                            else:
                                try:
                                    conn = sqlite3.connect("SIS.db")
                                    c = conn.cursor() 
                                    c.execute("PRAGMA foreign_keys = ON")                                                                                                                                        
                                    c.execute("INSERT INTO students(StudentIDNumber, StudentLastName, StudentFirstName, StudentMiddleInitial, CourseCode, StudentYearLevel, StudentGender) VALUES(?,?,?,?,?,?,?)",\
                                             (StudentIDNumber.get(),StudentLastName.get(),StudentFirstName.get(),StudentMiddleInitial.get(), CourseCode.get(),StudentYearLevel.get(),StudentGender.get()))                                        
                                    conn.commit()
                                    tkinter.messagebox.showinfo("Student Information System", "Student Recorded Successfully") 
                                    Clear()
                                    displayData()
                                    conn.close()
                                except:
                                    studentID=[]
                                    conn = sqlite3.connect("SIS.db")
                                    c = conn.cursor()
                                    c.execute("SELECT * FROM students")
                                    rows = c.fetchall()
                                    for row in rows:
                                        studentID.append(row[0])
                                    if studentID in studentID:
                                        tkinter.messagebox.showerroe("Student Information System", "ID Number already exists")
                                    else:    
                                        tkinter.messagebox.showerror("Student Information System", "Course Unavailable")
                    else:
                        tkinter.messagebox.showerror("Student Information System", "Invalid ID")
                else:
                    tkinter.messagebox.showerror("Student Information System", "Invalid ID")
        
        #======== CLEAR INPUT DATA BY USER ==========#
        
        def Clear():
            StudentIDNumber.set("")
            StudentFirstName.set("")
            StudentMiddleInitial.set("")
            StudentLastName.set("")
            StudentYearLevel.set("")
            StudentGender.set("")
            CourseCode.set("")
        
        #========= DISPLAY STUDENT DATA ===========#
        
        def displayData():
            try:
                tree.delete(*tree.get_children())
                conn = sqlite3.connect("SIS.db")
                cur = conn.cursor()
                cur.execute("PRAGMA foreign_keys = ON")
                cur.execute("SELECT * FROM students")
                rows = cur.fetchall()
                for row in rows:
                    tree.insert("", tk.END, text=row[0], values=row[0:])
                conn.close()
            except:
                pass
                    
        #========== DELETE STUDENT =============#
        
        def deleteData():
            messageDelete = tkinter.messagebox.askyesno("Student Information System", "Are you sure to delete Student Record?")
            if messageDelete > 0:   
                conn = sqlite3.connect("SIS.db")
                c = conn.cursor()
                x = tree.selection()[0]
                id_no = tree.item(x)["values"][0]
                c.execute("DELETE FROM students WHERE StudentIDNumber = ?",(id_no,))                   
                conn.commit()
                tree.delete(x)
                tkinter.messagebox.showinfo("Student Information System", "Student Record Deleted Successfully")
                displayData()
                conn.close()    
           
        #============= SEARCH STUDENT ===========#
        
        def searchData():
            StudentIDNumber = searchbar.get()             
            conn = sqlite3.connect("SIS.db")
            c = conn.cursor()
            c .execute("PRAGMA foreign_keys = ON")
            c.execute("SELECT * FROM students")
            conn.commit()
            tree.delete(*tree.get_children())
            rows = c.fetchall()
            for row in rows:
                if row[0].startswith(StudentIDNumber):
                    tree.insert("", tk.END, text=row[0], values=row[0:])
            conn.close()           
        
        #=========== SELECT STUDENT ============#
        
        def editData():
            if tree.focus() == "":
                tkinter.messagebox.showerror("Student Information System", "Please select a student record from the table")
                return
            values = tree.item(tree.focus(), "values")
            StudentIDNumber.set(values[0])
            StudentLastName.set(values[1])
            StudentFirstName.set(values[2])
            StudentMiddleInitial.set(values[3])
            CourseCode.set(values[4]) 
            StudentYearLevel.set(values[5])
            StudentGender.set(values[6])

        #========= UPDATE STUDENT ==============#
       
        def updateData():
            try:
                for selected in tree.selection():
                    conn = sqlite3.connect("SIS.db")
                    c = conn.cursor()
                    c.execute("PRAGMA foreign_keys = ON")
                    c.execute("UPDATE students SET StudentIDNumber=?, StudentLastName=?, StudentFirstName=?, StudentMiddleInitial=?,CourseCode=?, StudentYearLevel=?,StudentGender=?\
                          WHERE StudentIDNumber=?", (StudentIDNumber.get(),StudentLastName.get(),StudentFirstName.get(),StudentMiddleInitial.get(), CourseCode.get(),StudentYearLevel.get(),StudentGender.get(),\
                              tree.set(selected, '#1')))
                    conn.commit()
                    tkinter.messagebox.showinfo("Student Information System", "Student Record Updated Successfully")
                    displayData()
                    Clear()
                    conn.close()
            except:
                tkinter.messagebox.showerror("Student Information System", "Cannot update course")
                     
#============================ DESIGN ==============================#
        ##### FRAME #####
        LeftFrame = Frame(self, width=250, height=800, padx=2, bg="#a39193", relief=RIDGE)
        LeftFrame.pack(side=LEFT)
        topFrame = Frame(self, width=1350, height=30, padx=2, bg="#66545e", relief=RIDGE)
        topFrame.pack(side=TOP)
        
        #========== LABELS & ENTRIES ===========#
        
        self.lblStudentID = Label(self, font=('helvetica',12,'bold'), text="ID Number", bd=7 , anchor=W)
        self.lblStudentID.place(x=275,y=75)
        self.txtStudentID = Entry(self, font=('helvetica',12,'bold'), width=30, justify='left', textvariable = StudentIDNumber)
        self.txtStudentID.place(x=390,y=80)
        self.txtStudentID.insert(0,'YYYY-NNNN')
    
        self.lblLastName = Label(self, font=('helvetica',12,'bold'), text="Last Name ", bd=7, anchor=W)
        self.lblLastName.place(x=275,y=105)
        self.txtLastName = Entry(self, font=('helvetica',12,'bold'), width=30, justify='left', textvariable = StudentLastName)
        self.txtLastName.place(x=390,y=110)
    
        self.lblFirstName = Label(self, font=('helvetica',12,'bold'), text="First Name", bd=7, anchor=W)
        self.lblFirstName.place(x=275,y=135)
        self.txtFirstName = Entry(self, font=('helvetica',12,'bold'), width=30, justify='left', textvariable = StudentFirstName)
        self.txtFirstName.place(x=390,y=140)
        
        self.lblMiddleName = Label(self, font=('helvetica',12,'bold'), text="Middle Initial", bd=7, anchor=W)
        self.lblMiddleName.place(x=275,y=165)
        self.txtMiddleName = Entry(self, font=('helvetica',12,'bold'), width=30, justify='left', textvariable = StudentMiddleInitial)
        self.txtMiddleName.place(x=390,y=170)
            
        self.lblCourse = Label(self, font=('helvetica',12,'bold'), text="Course Code", bd=7, anchor=W)
        self.lblCourse.place(x=275,y=195)
        self.txtCourse = Entry(self, font=('helvetica',12,'bold'), width=30, justify='left', textvariable = CourseCode)
        self.txtCourse.place(x=390,y=200)
            
        self.lblGender = Label(self, font=('helvetica',12,'bold'), text="Gender", bd=7, anchor=W)
        self.lblGender.place(x=275,y=225)
        self.cboGender = ttk.Combobox(self, font=('helvetica',12,'bold'), state='readonly', width=28, textvariable = StudentGender)
        self.cboGender['values'] = ('Female', 'Male')
        self.cboGender.place(x=390,y=230)
        
        self.lblYearLevel = Label(self, font=('helvetica',12,'bold'), text="Year Level", bd=7, anchor=W)
        self.lblYearLevel.place(x=275,y=255)
            
        self.cboYearLevel = ttk.Combobox(self, font=('helvetica',12,'bold'), state='readonly', width=28, textvariable = StudentYearLevel)
        self.cboYearLevel['values'] = ('1st Year', '2nd Year', '3rd Year', '4th Year')
        self.cboYearLevel.place(x=390,y=260)
            
        self.searchbar = Entry(self, font=('helvetica',12,'bold'), textvariable = searchbar, width = 25)
        self.searchbar.place(x=680,y=45)
        self.searchbar.insert(0,'Enter ID Number')
            
        
        self.title = Label(LeftFrame, font=("rockwell", 55), bg="#a39193",text="SIS", fg="snow")
        self.title.place(x=40,y=10)    
        
        #=========== BUTTONS ==============#
        
        
        self.btnAddNew=Button(self, pady=1,bd=4,font=('helvetica',12,'bold'), padx=24, width=10, text='Add New Student', bg="#7f5539", fg="snow", command=addStudent)
        self.btnAddNew.place(x=280,y=320)
            
        self.btnClear=Button(self, pady=1,bd=4,font=('helvetica',12,'bold'), padx=24, width=10, text='Clear Fields', bg="#7f5539", fg="snow", command=Clear)
        self.btnClear.place(x=500,y=320)
                
        self.btnUpdate=Button(self, pady=1,bd=4,font=('helvetica',12,'bold'), padx=24, width=10, text='Update Student', bg="#7f5539",fg="snow", command=updateData)
        self.btnUpdate.place(x=500,y=380)

        self.btnEdit=Button(self, pady=1,bd=4,font=('helvetica',12,'bold'), padx=24, width=10, text='Edit Student', bg="#7f5539", fg="snow", command = editData)
        self.btnEdit.place(x=280,y=380)

        self.btnDelete=Button(self, pady=1,bd=4,font=('helvetica',12,'bold'), padx=24, width=10, text='Delete Student',bg="#7f5539", fg="snow", command = deleteData)
        self.btnDelete.place(x=380,y=440)

        self.btnSearch=Button(self,bd=1,font=('helvetica',12,'bold'), width=10, text='Search', bg="#7f5539",fg="snow", command = searchData)
        self.btnSearch.place(x=920,y=41)
        
        self.btnShowAll=Button(self,bd=1,font=('helvetica',12,'bold'), width=10, text='Show All', bg="#7f5539", fg="snow", command = displayData)
        self.btnShowAll.place(x=1100,y=41)
        
        #========= Window Buttons ==========#
        
        button1 = tk.Button(self, text="DASHBOARD",font=("rockwell",18),bd=0,
                            bg="#a39193",
                            fg="snow",
                            command=lambda: controller.show_frame(Dashboard))
        button1.place(x=40,y=160)
        button1.config(cursor= "hand2")

        button2 = tk.Button(self, text="STUDENTS",font=("rockwell",18),bd=0,
                            bg="#a39193",
                            fg="snow",
                            command=lambda: controller.show_frame(Students))
        button2.place(x=40,y=260)
        button2.config(cursor= "hand2")
        
        button3 = tk.Button(self, text="COURSE",font=("rockwell",18),bd=0,
                            bg="#a39193",
                            fg="snow",
                            command=lambda: controller.show_frame(Course))
        button3.place(x=40,y=360)
        button3.config(cursor= "hand2")
        
        scroll_y=Scrollbar(self, orient=VERTICAL)
    
        tree = ttk.Treeview(self, height=20, columns=("ID Number", "Last Name", "First Name", "Middle Initial", "Course", "Year Level", "Gender"), yscrollcommand=scroll_y.set)
    
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.place(x=1328,y=79,height=388)
        
        tree.heading("ID Number", text="ID Number")
        tree.heading("Last Name", text="Last Name")
        tree.heading("First Name", text="First Name")
        tree.heading("Middle Initial", text="Middle Initial")   
        tree.heading("Course", text="Course")
        tree.heading("Year Level", text="Year Level")
        tree.heading("Gender", text="Gender")
        tree['show'] = 'headings'
    
        tree.column("ID Number", width=90)
        tree.column("Last Name", width=100)
        tree.column("First Name", width=130)
        tree.column("Middle Initial", width=80)
        tree.column("Course", width=90)
        tree.column("Year Level", width=70)
        tree.column("Gender", width=60)
        scroll_y.config(command=tree.yview)
        tree.pack(fill=BOTH,expand=1)
        tree.place(x=680, y=79)
        
        displayData()  

app = SSIS()
app.geometry("1350x550+0+0")
app.mainloop()


