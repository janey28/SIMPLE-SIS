#Author: Jane Ann Telmoso
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
import tkinter.ttk as ttk
import csv
import os
import sys


class Student:

    def __init__(self, root):
        self.root = root
        blank_space = ""
        self.root.title(200 * blank_space + "Student Information System")
        self.root.geometry("1120x640+0+0")
        self.root.resizable(False, False)
        self.data = dict()
        self.temp = dict()
        self.filename = "SIS.csv"

        StudentFirstName = StringVar()
        StudentMiddleInitial = StringVar()
        StudentLastName = StringVar()
        StudentIDNumber = StringVar()
        StudentYearLevel = StringVar()
        StudentGender = StringVar()
        StudentCourse = StringVar()
        searchbar = StringVar()

        if not os.path.exists('SIS.csv'):
            with open('SIS.csv', mode='w') as csv_file:
                fieldnames = ["Student ID Number", "Last Name", "First Name", "Middle Initial", "Course", "Year Level",
                              "Gender"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writeheader()

        else:
            with open('SIS.csv', newline='') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    self.data[row["Student ID Number"]] = {'Last Name': row["Last Name"],
                                                           'First Name': row["First Name"],
                                                           'Middle Initial': row["Middle Initial"],
                                                           'Course': row["Course"],
                                                           'Year Level': row["Year Level"],
                                                           'Gender': row["Gender"]}
            self.temp = self.data.copy()

        ##### ADD STUDENT ####

        def addStudent():
            with open('SIS.csv', "a", newline="") as file:
                csvfile = csv.writer(file)
                if StudentIDNumber.get() == "" or StudentFirstName.get() == "" or StudentMiddleInitial.get() == "" or StudentLastName.get() == "" or StudentYearLevel.get() == "" or StudentGender.get() == "" or StudentCourse.get() == "":
                    tkinter.messagebox.showinfo("Student Information System", "Please fill in the box.")
                else:
                    studentID = StudentIDNumber.get()
                    studentID_list = []
                    for i in studentID:
                        studentID_list.append(i)
                    if "-" in studentID_list:
                        x = studentID.split("-")
                        y = x[0]
                        n = x[1]
                        if y.isdigit() == False or n.isdigit() == False:
                            tkinter.messagebox.showerror("Student Information System", "Invalid ID Number")
                        else:
                            if studentID in self.data:
                                tkinter.messagebox.showinfo("Student Information System", "Student already exists")
                            else:
                                self.data[StudentIDNumber.get()] = {'Last Name': StudentLastName.get(),
                                                                    'First Name': StudentFirstName.get(),
                                                                    'Middle Initial': StudentMiddleInitial.get(),
                                                                    'Course': StudentCourse.get(),
                                                                    'Year Level': StudentYearLevel.get(),
                                                                    'Gender': StudentGender.get()}
                                self.saveData()
                                tkinter.messagebox.showinfo("Student Information System", "Student Data Recorded Successfully")
                                Clear()
                    else:
                        tkinter.messagebox.showerror("Student Information System", "Invalid ID Number")
                displayData()

        ##### CLEAR INPUT DATA BY USER ####

        def Clear():
            StudentIDNumber.set("")
            StudentFirstName.set("")
            StudentMiddleInitial.set("")
            StudentLastName.set("")
            StudentYearLevel.set("")
            StudentGender.set("")
            StudentCourse.set("")

        ##### DISPLAY DATA #####

        def displayData():
            tree.delete(*tree.get_children())
            with open('SIS.csv') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    IDNumber = row['Student ID Number']
                    LastName = row['Last Name']
                    FirstName = row['First Name']
                    MiddleInitial = row['Middle Initial']
                    Course = row['Course']
                    YearLevel = row['Year Level']
                    Gender = row['Gender']
                    tree.insert("", 0, values=(IDNumber, LastName, FirstName, MiddleInitial, Course, YearLevel, Gender))

        ##### DELETE STUDENT #####

        def deleteData():
            if tree.focus() == "":
                tkinter.messagebox.showerror("Student Information System",
                                             "Please select a student record from the table")
                return
            id_no = tree.item(tree.focus(), "values")[0]

            decision = tkinter.messagebox.askquestion("Student Information System", "Are you sure to delete Student Record?")
            if decision == "yes":
                self.data.pop(id_no, None)
                self.saveData()
                tree.delete(tree.focus())
                tkinter.messagebox.showinfo("Student Information System", "Student Record Deleted Successfully")
            else:
                pass

        ##### SEARCH STUDENT #####

        def searchData():
            s = self.searchbar.get()
            s_list = []
            for i in s:
                s_list.append(i)

            if "-" in s_list:
                x = s.split("-")
                y = x[0]
                n = x[1]
                if y.isdigit() == False or n.isdigit() == False:
                    tkinter.messagebox.showerror("Student Information System", "Invalid ID Number")
                else:
                    if s in self.data:
                        vals = list(self.data[self.searchbar.get()].values())
                        tree.delete(*tree.get_children())
                        tree.insert("", 0,
                                    values=(self.searchbar.get(), vals[0], vals[1], vals[2], vals[3], vals[4], vals[5]))
                    elif s == "":
                        displayData()
                    else:
                        tkinter.messagebox.showerror("Student Information System", "Student not found")
                        return
            elif s == "":
                tkinter.messagebox.showerror("Student Information System", "Student not found")
                return
            else:
                tkinter.messagebox.showerror("Student Information System", "Student not found")
                return

        ##### SELECT STUDENT #####

        def editData():
            if tree.focus() == "":
                tkinter.messagebox.showerror("Student Information System",
                                             "Please select a student record from the table")
                return
            values = tree.item(tree.focus(), "values")
            StudentIDNumber.set(values[0])
            StudentLastName.set(values[1])
            StudentFirstName.set(values[2])
            StudentMiddleInitial.set(values[3])
            StudentGender.set(values[4])
            StudentYearLevel.set(values[5])
            StudentCourse.set(values[6])

        ##### UPDATE STUDENT #####

        def updateData():
            with open('SIS.csv', "a", newline="") as file:
                csvfile = csv.writer(file)
                if StudentIDNumber.get() == "" or StudentFirstName.get() == "" or StudentMiddleInitial.get() == "" or StudentLastName.get() == "" or StudentYearLevel.get() == "":
                    tkinter.messagebox.showinfo("Student Information System",
                                                "Please select a student record from the table")
                else:
                    self.data[StudentIDNumber.get()] = {'Last Name': StudentLastName.get(),
                                                        'First Name': StudentFirstName.get(),
                                                        'Middle Initial': StudentMiddleInitial.get(),
                                                        'COurse': StudentCourse.get(),
                                                        'Year Level': StudentYearLevel.get(),
                                                        'Gender': StudentGender.get()}
                    self.saveData()
                    tkinter.messagebox.showinfo("Student Information System", "Student Record Updated Successfully")
                Clear()
                displayData()

            # ============================ DESIGN ==============================#

        ##### FRAME #####
        BottomFrame = Frame(self.root, width=1500, height=700, padx=2, bg="#66545e", relief=RIDGE)
        BottomFrame.place(x=0, y=0)

        TitleFrame = Frame(self.root, width=1500, height=100, padx=2, bg="#a39193", relief=RIDGE)
        TitleFrame.place(x=0, y=0)


        ##### LABELS & ENTRIES #####
        self.lblTitle = Label(self.root, font=('rockwell', 30, 'bold'), text="STUDENT INFORMATION SYSTEM", bg = "#a39193", fg = "snow", bd=7, anchor=W)
        self.lblTitle.place(x=220, y=15)

        self.lblStudentdetails = Label(self.root, text = "Student Details", bg = "#996f73", fg = "snow", font = ("helvetica", 20, "bold"))
        self.lblStudentdetails.place(x=80, y=110)

        self.lblStudentID = Label(self.root, font=('helvetica', 12, 'bold'), text="ID Number", bd=7, anchor=W)
        self.lblStudentID.place(x=30, y=170)
        self.txtStudentID = Entry(self.root, font=('helvetica', 12, 'bold'), width=20, justify='left',
                                  textvariable=StudentIDNumber)
        self.txtStudentID.place(x=160, y=175)
        self.txtStudentID.insert(0, 'YYYY-NNNN')

        self.lblLastName = Label(self.root, font=('helvetica', 12, 'bold'), text="Last Name", bd=7, anchor=W)
        self.lblLastName.place(x=30, y=210)
        self.txtLastName = Entry(self.root, font=('helvetica', 12, 'bold'), width=20, justify='left',
                                 textvariable=StudentLastName)
        self.txtLastName.place(x=160, y=215)

        self.lblFirstName = Label(self.root, font=('helvetica', 12, 'bold'), text="First Name", bd=7, anchor=W)
        self.lblFirstName.place(x=30, y=250)
        self.txtFirstName = Entry(self.root, font=('helvetica', 12, 'bold'), width=20, justify='left',
                                  textvariable=StudentFirstName)
        self.txtFirstName.place(x=160, y=255)

        self.lblMiddleInitial = Label(self.root, font=('helvetica', 12, 'bold'), text="Middle Initial", bd=7, anchor=W)
        self.lblMiddleInitial.place(x=30, y=290)
        self.txtMiddleInitial = Entry(self.root, font=('helvetica', 12, 'bold'), width=20, justify='left',
                                      textvariable=StudentMiddleInitial)
        self.txtMiddleInitial.place(x=160, y=295)

        self.lblCourse = Label(self.root, font=('helvetica', 12, 'bold'), text="Course", bd=7, anchor=W)
        self.lblCourse.place(x=30, y=330)
        self.txtCourse = Entry(self.root, font=('helvetica', 12, 'bold'), width=20, justify='left',
                               textvariable=StudentCourse)
        self.txtCourse.place(x=160, y=335)

        self.lblGender = Label(self.root, font=('helvetica', 12, 'bold'), text="Gender", bd=7, anchor=W)
        self.lblGender.place(x=30, y=410)

        self.cboGender = ttk.Combobox(self.root, font=('helvetica', 12, 'bold'), state='readonly', width=10,
                                      textvariable=StudentGender)
        self.cboGender['values'] = ('Female', 'Male')
        self.cboGender.place(x=160, y=415)

        self.lblYearLevel = Label(self.root, font=('helvetica', 12, 'bold'), text="Year Level", bd=7, anchor=W)
        self.lblYearLevel.place(x=30, y=370)

        self.cboYearLevel = ttk.Combobox(self.root, font=('helvetica', 12, 'bold'), state='readonly', width=10,
                                         textvariable=StudentYearLevel)
        self.cboYearLevel['values'] = ('1st Year', '2nd Year', '3rd Year', '4th Year')
        self.cboYearLevel.place(x=160, y=375)

        self.searchbar = Entry(self.root, font=('helvetica', 12, 'bold'), textvariable=searchbar, width=25)
        self.searchbar.place(x=460, y=125)
        self.searchbar.insert(0, 'Enter ID Number')

        ##### BUTTONS #####

        self.btnAddNew = Button(self.root, pady=1, bd=4, font=('helvetica', 11, 'bold'), padx=24, width=9,
                                text='Add New Student', bg="#7f5539",fg = "snow", command=addStudent)
        self.btnAddNew.place(x=40, y=465)

        self.btnClear = Button(self.root, pady=1, bd=4, font=('helvetica', 11, 'bold'), padx=24, width=8, text='Clear Fields',
                               bg="#7f5539",fg = "snow", command=Clear)
        self.btnClear.place(x=200, y=465)

        self.btnUpdate = Button(self.root, pady=1, bd=4, font=('helvetica', 11, 'bold'), padx=24, width=8, text='Update Student',
                                bg="#7f5539", fg = "snow", command=updateData)
        self.btnUpdate.place(x=200, y=515)

        self.btnEdit = Button(self.root, pady=1, bd=4, font=('helvetica', 11, 'bold'), padx=28, width=8,
                              text='Edit Student', bg="#7f5539",fg = "snow", command=editData)
        self.btnEdit.place(x=40, y=515)

        self.btnDelete = Button(self.root, pady=1, bd=4, font=('helvetica', 11, 'bold'), padx=24, width=8, text='Delete Student',
                                bg="#7f5539", fg = "snow", command=deleteData)
        self.btnDelete.place(x=120, y=565)

        self.btnSearch = Button(self.root, bd=1, font=('helvetica', 12, 'bold'), width=10, text='Search', bg="#7f5539",fg = "snow",
                                command=searchData)
        self.btnSearch.place(x=710, y=120)

        self.btnShowAll = Button(self.root, bd=1, font=('helvetica', 12, 'bold'), width=10, text='Show All', bg="#7f5539",fg = "snow",
                                 command=displayData)
        self.btnShowAll.place(x=850, y=120)

        scroll_y = Scrollbar(self.root, orient=VERTICAL)
        # scroll_y.grid(row=1, column=1, sticky='ns')

        tree = ttk.Treeview(self.root, height=20, columns=(
        "Student ID Number", "Last Name", "First Name", "Middle Initial", "Course", "Year Level", "Gender"),
                            yscrollcommand=scroll_y.set)

        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_y.place(x=1072, y=171, height=424)

        tree.heading("Student ID Number", text="Student ID Number")
        tree.heading("Last Name", text="Last Name")
        tree.heading("First Name", text="First Name")
        tree.heading("Middle Initial", text="Middle Initial")
        tree.heading("Course", text="Course")
        tree.heading("Year Level", text="Year Level")
        tree.heading("Gender", text="Gender")
        tree['show'] = 'headings'

        tree.column("Student ID Number", width=120)
        tree.column("Last Name", width=100)
        tree.column("First Name", width=150)
        tree.column("Middle Initial", width=100)
        tree.column("Course", width=90)
        tree.column("Year Level", width=70)
        tree.column("Gender", width=70)
        scroll_y.config(command=tree.yview)
        tree.pack(fill=BOTH, expand=1)
        tree.place(x=370, y=170)
        displayData()

    def saveData(self):
        temps = []
        with open('SIS.csv', "w", newline='') as update:
            fieldnames = ["Student ID Number", "Last Name", "First Name", "Middle Initial", "Course", "Year Level",
                          "Year Level"]
            writer = csv.DictWriter(update, fieldnames=fieldnames, lineterminator='\n')
            writer.writeheader()
            for id, val in self.data.items():
                temp = {"Student ID Number": id}
                for key, value in val.items():
                    temp[key] = value
                temps.append(temp)
            writer.writerows(temps)


if __name__ == '__main__':
    root = Tk()
    application = Student(root)
    root.mainloop()
