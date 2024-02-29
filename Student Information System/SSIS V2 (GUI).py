import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import *
import csv
import re

# ------------------------------------- MAIN PAGE / TAB ------------------------------------------------ #


root = tk.Tk()
root.geometry("1200x600") #1300x550
root.resizable(False,False)
root.title("STUDENT INFORMATION SYSTEM")

systemTitle = Label(root, text ='STUDENT INFORMATION MANAGEMENT SYTEM', font =('Arial',18,'bold'), relief=GROOVE,borderwidth=1,height=1,width=600, bg='GREEN',fg='white')
systemTitle.pack()

developerTitle = Label(root,text='Developed by SNEQ', font=('Arial',7,'bold'),relief=GROOVE,borderwidth=1,height=1,width=2, bg='GREEN',fg='WHITE')
developerTitle.pack(side=BOTTOM,fill=tk.X)

# -------------------------------------- M A I N  F R A M E S ----------------------------------------------------- #

# Options/Choices Frame for Buttons (where functional buttons like ADD, DELETE, & EDIT will be located)
optionsFrame = ttk.Frame(root,relief=GROOVE,borderwidth=5)
optionsFrame.place(x=25,y=50,width=200,height=530)

# Student Database Frame (where the displayed StudentList.csv file will be located)
databaseFrame = ttk.Frame(root,relief=GROOVE,borderwidth=5)
databaseFrame.place(x=250,y=50,width=930,height=530)

# -------------------------------------- S T U D E N T D A T A B A S E ----------------------------------------------------- #

yScrollbar = Scrollbar(databaseFrame,orient=VERTICAL)
# Treeview widget to display the data from CSV file
studentDatabase = ttk.Treeview(databaseFrame,columns=(1,2,3,4,5,6),show="headings",height="25",yscrollcommand=yScrollbar.set)
yScrollbar.pack(side=RIGHT,fill=Y)
yScrollbar.config(command=studentDatabase.yview)
#tree = ttk.Treeview(databaseFrame,columns=(1,2,3,4,5,6),show="headings",height="25")
studentDatabase.pack(fill=BOTH,expand=1)
#grid(row=0, column=1, pady=10, sticky='nsew')

# Configure the column headings
studentDatabase.heading(1, text="Last Name")
studentDatabase.column(1,width=200)
studentDatabase.heading(2, text="First Name")
studentDatabase.column(2,width=200)
studentDatabase.heading(3, text="Gender")
studentDatabase.column(3,width=75)
studentDatabase.heading(4, text="ID Number")
studentDatabase.column(4,width=100)
studentDatabase.heading(5, text="Year Level")
studentDatabase.column(5,width=70)
studentDatabase.heading(6, text="Course Code")
studentDatabase.column(6,width=100)

# Predefined rows for CSV file
predefined_rows = ["Last Name", "First Name", "Sex", "Year Level", "ID Number", "Course Code"] #code that adds the field names in csv file when the csv file is empty
with open("StudentList.csv", "r") as student_file:
    reader = csv.reader(student_file)
    if predefined_rows != next(reader):
        with open("StudentList.csv", "w", newline="") as student_file:
            writer = csv.writer(student_file)
            writer.writerow(predefined_rows)

# ------------------------------------- F U N C T I O N S ------------------------------------------------ #
def loadStudentData():
    # Read the CSV file and add the data to the treeview widget
    with open("StudentList.csv", "r") as student_file:
        reader = csv.reader(student_file)
        headers = next(reader)
        for row in reader:
            studentDatabase.insert("", "end", values=row)
loadStudentData()

def updateTreeview():
    for record in studentDatabase.get_children():
        studentDatabase.delete(record)

    with open("StudentList.csv","r") as student_file:
        reader = csv.reader(student_file)
        next(reader) #skips header
        for row in reader:
            studentDatabase.insert("", "end", values=row)

def home(): # function that leads the user to the main page / tab
    addButtonMain.pack()
    delButton.pack()
    editButton.pack()
    viewCoursesButton.pack()
    exitButton.pack()
    optionsFrame.place(x=25,y=50,width=200,height=530)
    databaseFrame.place(x=250,y=50,width=930,height=530)
    studentDetailsFrame.destroy()
    addStudentFrame.destroy()

        
def exit():
    print("Exiting...")
    root.destroy()
    
def addStudentPage():

    # ---------------------- FRAMES USED IN ADD STUDENT PAGE / TAB --------------------------------------- #

    global addStudentFrame
    addStudentFrame = ttk.Frame(root)

    global studentDetailsFrame
    studentDetailsFrame = ttk.Frame(root,relief=GROOVE,borderwidth=5)
    studentDetailsFrame.place(x=25,y=50,width=280,height=530)

    databaseFrame.place(x=320,y=50,width=850,height=530)

    # Additional Frames to make Rows to place the labels and entry fields in the Add Student Page
    lastName_row = tk.Frame(studentDetailsFrame)
    lastName_row.pack(side=tk.TOP, fill=tk.X)

    firstName_row = tk.Frame(studentDetailsFrame)
    firstName_row.pack(side=tk.TOP, fill=tk.X)

    sexualOrientation_row = tk.Frame(studentDetailsFrame)
    sexualOrientation_row.pack(side=tk.TOP, fill=tk.X)

    yearLevel_row = tk.Frame(studentDetailsFrame)
    yearLevel_row.pack(side=tk.TOP, fill=tk.X)

    idNum_row = tk.Frame(studentDetailsFrame)
    idNum_row.pack(side=tk.TOP, fill=tk.X)

    courseCode_row = tk.Frame(studentDetailsFrame)
    courseCode_row.pack(side=tk.TOP, fill=tk.X)
    
    # ------------------------------------ F U N C T I O N S ------------------------------------------------- #

    def addStudent(): #this function adds the neccessary information of the student to a csv file by asking the user for input
        
        # Getting the Inputs
        lastName = lastName_entry.get()
        firstName = firstName_entry.get()
        sexualOrientation = sexualOrientation_combo.get()
        yearLevel = yearLevel_entry.get()
        idNum = idNum_entry.get()
        courseCode = courseCode_entry.get()

        # Checks if any of the entry fields are blank or empty
        if not(lastName and firstName and sexualOrientation and yearLevel and idNum):
            messagebox.showerror("Error","All fields must be filled.")
            return

        # Validates the year level input
        while True:
            try:
                yearLevel = int(yearLevel)
                if 1 <= yearLevel <= 4: #checks if year level input is valid
                    pass
                else:
                    messagebox.showerror("Invalid Year Level Input", "Oops! Enter a valid year level (1 to 4 only)")
                    return
            except ValueError:
                messagebox.showerror("Invalid Year Level Input", "Oops! Enter a valid year level (1 to 4 only)")   
                return
            
        # Validates the course code input if it exists or not
            with open('CourseList.csv', 'r') as course_file:
                reader = csv.reader(course_file) #reads the CourseList.csv file
                courses = [row[0] for row in reader]

            if courseCode in courses: #checks whether user input of the student's course is found from the course list (valid)
                print(f"Course Name: {courses[0]}")
                break #exits the loop once the course is found from the CourseList.csv file
            elif courseCode == '': #if course input is empty
                print ('N/A')
                break
            else:
                messagebox.showerror('Course Not Available! Please try again.')   
                print ('Unenrolled')
                return

        with open("StudentList.csv", "r") as student_file: #checks for any duplicates before adding the student
            reader = csv.reader(student_file)
            students = [row for row in reader]

        if [lastName,firstName,idNum,sexualOrientation,str(yearLevel),courseCode] not in students:
            with open("StudentList.csv", "a", newline='') as student_file:
                writer = csv.writer(student_file)
                writer.writerow([lastName,firstName,sexualOrientation,idNum,yearLevel,courseCode])
                messagebox.showinfo("Student Added","Student added successfully!")
                updateTreeview()
                # Clears all the previous field inputs by the user after adding the student successfully
                lastName_entry.delete(0, 'end')
                firstName_entry.delete(0, 'end')
                sexualOrientation_combo.set('')
                yearLevel_entry.delete(0, 'end')
                idNum_entry.delete(0, 'end')
                courseCode_entry.delete(0, 'end')
        else:
            messagebox.showinfo("Student already exists in the list. No duplicates allowed.")

        # Validates the input format for ID Number
        idNumFormat = r"\d{4}-\d{4}"
        idNumLength = 9

        while True:
            try:
                if re.match(idNumFormat,idNum) and len(idNum) == idNumLength and all(c.isdigit() or c == '-' for c in idNum):
                    return idNum
                else:
                    messagebox.showerror("Invalid ID Number Format", "Oops! Enter a valid ID Number format (YYYY-NNNN, e.g. 2022 - 0001)")
                    break
            except ValueError:
                messagebox.showerror("Invalid ID Number Format", "Oops! Enter a valid ID Number format (YYYY-NNNN, e.g. 2022 - 0001)")
                break
        pass
            
    updateTreeview()

    # ------------------------------------- E N T R I E S ---------------------------------------------------- #

    # Labels and Entry Fields for User Inputs in Adding Students
        
    lastName = tk.Label(lastName_row, text="Last Name: ")
    lastName.pack(side=tk.LEFT,ipady=10)
    lastName_entry = tk.Entry(lastName_row)
    lastName_entry.pack(side=tk.LEFT,fill=tk.X, padx=20)

    firstName_label = tk.Label(firstName_row, text="First Name: ")
    firstName_label.pack(side=tk.LEFT,ipady=10)
    firstName_entry = tk.Entry(firstName_row)
    firstName_entry.pack(side=tk.LEFT,fill=tk.X,padx=19)

    sexualOrientation_label = tk.Label(sexualOrientation_row, text="Sex: ")
    sexualOrientation_label.pack(side=tk.LEFT,padx=15,ipady=10)
    sexualOrientation_combo = ttk.Combobox(sexualOrientation_row, values=["Male","Female"],state="readonly")
    sexualOrientation_combo.pack(side=tk.LEFT,padx=27,ipadx=0)

    yearLevel_label = tk.Label(yearLevel_row, text="Year Level: ")
    yearLevel_label.pack(side=tk.LEFT)
    yearLevel_entry = tk.Entry(yearLevel_row)
    yearLevel_entry.pack(side=tk.LEFT,fill=tk.X)

    idNum_label = tk.Label(idNum_row, text="ID Number (YYYY - ####): ")
    idNum_label.pack(side=tk.LEFT)
    idNum_entry = tk.Entry(idNum_row)
    idNum_entry.pack(side=tk.LEFT,fill=tk.X)

    courseCode_label = tk.Label(courseCode_row, text="Course Code (ex. BSCS): ")
    courseCode_label.pack(side=tk.LEFT)

    # Read course codes from CourseList.csv
    with open("CourseList.csv", "r") as course_file:
        reader = csv.reader(course_file)
        next(reader) # skips header
        courseCodes = [row[0] for row in reader]

    courseCode_combo = ttk.Combobox(courseCode_row,values=courseCodes,state="readonly")
    courseCode_combo.pack(side=tk.LEFT,fill=tk.X)

    # ----------------------------- B U T T O N S ----------------------------------------------------- #
    homeButton = Button( # HOME Button
        studentDetailsFrame, 
        background='#0055D8',
        foreground='WHITE',
        activebackground='#30ECFF',
        activeforeground='BLACK',
        width=15,
        height=0,
        border=1,
        cursor='hand1',
        text = "HOME",
        font=('Arial', 12, 'bold'),
        command=home)
    homeButton.pack(side=BOTTOM)

    addButton = Button( # ADD Button (for Add Student page/tab)
        studentDetailsFrame, 
        background='#00B64E',
        foreground='WHITE',
        activebackground='#04F56B',
        activeforeground='WHITE',
        width=15,
        height=1,
        border=1,
        cursor='hand1',
        text = "ADD STUDENT",
        font=('Arial', 12, 'bold'),
        command=addStudent)
    addButton.pack(pady=15)

    addStudentFrame.pack()
    optionsFrame.pack_forget()
    databaseFrame.pack_forget()

def deleteStudent(): #this function enables the user to remove a selected student using its ID Number from the student list or database

    selectedStudent = studentDatabase.selection()
    if not selectedStudent: # this ensures that 
        messagebox.showerror("Error", "Please select a student to delete.")
        return
    
    values = studentDatabase.item(selectedStudent,"values")

    studentDatabase.delete(selectedStudent) # this enables the user to delete a selected item or student from the student database treeview

    with open("StudentList.csv", "r") as student_file:
        reader = csv.reader(student_file)
        rows = [row for row in reader if row != values]

    with open("StudentList.csv", "w", newline='') as student_file:
        writer = csv.writer(student_file)
        writer.writerows(rows)

    messagebox.showinfo("Student Deleted", "Student deleted successfully!")

def editStudent():

    selectedStudent = studentDatabase.selection()
    if not selectedStudent:
        messagebox.showerror("Error", "Please select a student to edit.")
        return
    
     # Get the selected student's current information
    currentValues = studentDatabase.item(selectedStudent, "values")

    # Pop-Up Window for Editing Student Details
    editStudent_window = tk.Tk()
    editStudent_window.resizable(False,False)
    editStudent_window.title("Edit Student")
    editStudent_window.geometry("300x280")

    # --------------------------------- E N T R I E S ------------------------------------#
    Label(editStudent_window, text="Last Name: ").grid(row=0, column=0, padx=5, pady=5)
    lastName= Entry(editStudent_window)
    lastName.insert(0, currentValues[0])
    lastName.grid(row=0, column=1, padx=5, pady=5)
    
    Label(editStudent_window, text="First Name: ").grid(row=1, column=0, padx=5, pady=5)
    firstName = Entry(editStudent_window)
    firstName.insert(0, currentValues[1])
    firstName.grid(row=1, column=1, padx=5, pady=5)

    Label(editStudent_window, text="Sex: ").grid(row=2, column=0, padx=5, pady=5)
    sexualOrientation = ttk.Combobox(editStudent_window,values=["Male","Female"])
    sexualOrientation.set(0, currentValues[2])
    sexualOrientation.grid(row=2, column=1, padx=5, pady=5)

    Label(editStudent_window, text="Year Level: ").grid(row=3, column=0, padx=5, pady=5)
    yearLevel_entry = Entry(editStudent_window)
    yearLevel_entry.insert(0, currentValues[3])
    yearLevel_entry.grid(row=3, column=1, padx=5, pady=5)

    Label(editStudent_window, text="ID Number: ").grid(row=4, column=0, padx=5, pady=5)
    idNum_entry = Entry(editStudent_window)
    idNum_entry.insert(0, currentValues[4])
    idNum_entry.grid(row=4, column=1, padx=5, pady=5)

    Label(editStudent_window, text="Course Code: ").grid(row=5, column=0, padx=5, pady=5)
    courseCode_entry = Entry(editStudent_window)
    courseCode_entry.insert(0, currentValues[5])
    courseCode_entry.grid(row=5, column=1, padx=5, pady=5)

    # -------------------------------- F U N C T I O N --------------------------------#
    def saveChanges():

        updatedDetails = [

            lastName.get(),
            firstName.get(),
            sexualOrientation.get(),
            yearLevel_entry.get(),
            idNum_entry.get(),
            courseCode_entry.get()
            
        ]

        studentDatabase.item(selectedStudent,values=updatedDetails) # updates the student data in treeview

        with open("StudentList.csv", "r") as file:
            reader = csv.reader(file)
            data = [row for row in reader]

        index = studentDatabase.index(selectedStudent)
        data[index] = updatedDetails

        with open("StudentList.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)

        messagebox.showinfo("Edit Student Success", "Student information updated successfully!")
        editStudent_window.destroy()

    def cancelChanges():

        editStudent_window.destroy()

    # ------------------------------- B U T T O N ----------------------------------- #
    
    saveButton = Button( # SAVE Button (for Edit Student Window)
    editStudent_window, 
    background='#0055D8',
    foreground='WHITE',
    activebackground='#30ECFF',
    activeforeground='BLACK',
    width=15,
    height=0,
    border=1,
    cursor='hand1',
    text = "SAVE",
    font=('Arial', 12, 'bold'),
    command=saveChanges)
    saveButton.grid(row=6, column=0, columnspan=2, padx=70, pady=10)

    cancelButton = Button( # CANCEL Button (for Edit Student Window)
    editStudent_window, 
    background='RED',
    foreground='WHITE',
    activebackground='PINK',
    activeforeground='BLACK',
    highlightthickness=1,
    width=15,
    height=0,
    border=1,
    cursor='hand1',
    text = "CANCEL",
    font=('Arial', 12, 'bold'),
    command=cancelChanges)
    cancelButton.grid(row=7, column=0, columnspan=2, padx=70, pady=2)

def viewCoursesPage():

# ------------ F R A M E S ------------------------------------------------ #
    viewCoursesFrame = ttk.Frame()
    
    global courseDatabaseFrame
    courseDatabaseFrame = ttk.Frame(root,relief=GROOVE,borderwidth=5)
    courseDatabaseFrame.place(x=25,y=50,width=1150,height=450)

    global courseOptionsFrame
    courseOptionsFrame = ttk.Frame(root,relief=GROOVE,borderwidth=5)
    courseOptionsFrame.place(x=25,y=510,width=1150,height=50)

# ---------------------------- C O U R S E  D A T A B A S E --------------- #
    
    courseDatabase = ttk.Treeview(courseDatabaseFrame, columns=(1, 2), show="headings")
    courseDatabase.heading(1, text="Course Code")
    courseDatabase.heading(2, text="Course Name")

    with open("CourseList.csv", "r") as course_file:
        reader = csv.reader(course_file)
        next(reader) #skips the headers
        for row in reader:
            courseDatabase.insert("", "end", values=row)

    courseDatabase.pack(fill="both", expand=True)

# ---------------------------- F U N C T I O N S ------------------------- #
    #def addCourse():

    def deleteCourse():

        selectedCourse = courseDatabase.selection()
        if not selectedCourse:
            messagebox.showerror("Error", "Please select a course to delete.")
            return
        
        courseDetails = courseDatabase.item(selectedCourse, "values")

        courseDatabase.delete(selectedCourse) # deletes course from course database treeview

        with open("CourseList.csv", "r") as course_file:
            reader = csv.reader(course_file)
            rows = [row for row in reader]

        rows_to_write = []
        for row in rows:
            if row != courseDetails:
                rows_to_write.append(row)

        with open("CourseList.csv", "w", newline="") as course_file:
            writer = csv.writer(course_file)
            writer.writerows(rows_to_write)

        messagebox.showinfo("Course Deleted", "Course deleted successfully!")

    viewCoursesFrame.pack()
    optionsFrame.destroy()
    databaseFrame.destroy() 

    #def editCourse():
    # ---------------------------- B U T T O N S ----------------------------- #
    
    addCourseButton = Button( # ADD Button to add a non-existing course to Course List
        courseOptionsFrame, 
        background='#00B64E',
        foreground='WHITE',
        activebackground='#04F56B',
        activeforeground='WHITE',
        width=20,
        height=1,
        border=1,
        cursor='hand1',
        text = "ADD NEW COURSE",
        font=('Arial', 12, 'bold'))
    addCourseButton.pack(side=LEFT,padx=15)

    delCourseButton = Button( # DELETE Button to delete an existing course from Course List
        courseOptionsFrame, 
        background='RED',
        foreground='WHITE',
        activebackground='PINK',
        activeforeground='BLACK',
        width=20,
        height=1,
        border=1,
        cursor='hand1',
        text = "DELETE A COURSE",
        font=('Arial', 12, 'bold'),
        command=deleteCourse)
    delCourseButton.pack(side=LEFT, padx=15)

    editCourseButton = Button( # EDIT Button to update or change any course detail (course code or course name or both)
        courseOptionsFrame, 
        background='YELLOW',
        foreground='BLACK',
        activebackground='#FFF93D',
        activeforeground='BLACK',
        width=20,
        height=1,
        border=1,
        cursor='hand1',
        text = "EDIT COURSE",
        font=('Arial', 12, 'bold'))
    editCourseButton.pack(side=LEFT,padx=15)

    homeButton = Button( # BACK Button
        courseOptionsFrame, 
        background='#0055D8',
        foreground='WHITE',
        activebackground='#30ECFF',
        activeforeground='BLACK',
        width=20,
        height=0,
        border=1,
        cursor='hand1',
        text = "HOME",
        font=('Arial', 12, 'bold'),
        command=home)
    homeButton.pack(side=RIGHT,padx=15)

# ------------------------------------- B U T T O N S (MAIN PAGE / TAB) ---------------------------------------------------- #

addButtonMain = Button( # ADD Button (for main page/tab)
    optionsFrame, 
    background='#00B64E',
    foreground='WHITE',
    activebackground='#04F56B',
    activeforeground='WHITE',
    width=25,
    height=2,
    border=1,
    cursor='hand1',
    text = "ADD STUDENT",
    font=('Arial', 14, 'bold'),
    command=addStudentPage)
addButtonMain.pack(pady=25)

delButton = Button( # DELETE Button
    optionsFrame, 
    background='RED',
    foreground='WHITE',
    activebackground='PINK',
    activeforeground='BLACK',
    highlightthickness=1,
    width=25,
    height=2,
    border=1,
    cursor='hand1',
    text = "DELETE STUDENT",
    font=('Arial', 14, 'bold'),
    command=deleteStudent)
delButton.pack()

editButton = Button( # EDIT Button
    optionsFrame, 
    background='YELLOW',
    foreground='BLACK',
    activebackground='#FFF93D',
    activeforeground='BLACK',
    highlightthickness=1,
    width=25,
    height=2,
    border=1,
    cursor='hand1',
    text = "EDIT STUDENT",
    font=('Arial', 14, 'bold'),
    command=editStudent)
editButton.pack()

viewCoursesButton = Button( # EDIT Button
    optionsFrame, 
    background='#504F4F',
    foreground='WHITE',
    activebackground='#A4A4A4',
    activeforeground='WHITE',
    highlightthickness=1,
    width=15,
    height=1,
    border=1,
    cursor='hand1',
    text = "VIEW COURSE",
    font=('Arial', 9, 'bold'),
    command=viewCoursesPage)
viewCoursesButton.pack(side=LEFT,anchor=tk.S)

exitButton = Button( # EDIT Button
    optionsFrame, 
    background='#E10000',
    foreground='WHITE',
    activebackground='#FF0909',
    activeforeground='WHITE',
    highlightthickness=1,
    width=10,
    height=1,
    border=1,
    cursor='hand1',
    text = "EXIT",
    font=('Arial', 9, 'bold'),
    command=exit)
exitButton.pack(side=LEFT,padx=5,anchor=tk.S)

root.mainloop()