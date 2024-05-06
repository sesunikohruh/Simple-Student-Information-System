import mysql.connector
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
studentDatabase = ttk.Treeview(databaseFrame,columns=(1,2,3,4,5,6,7),show="headings",height="25",yscrollcommand=yScrollbar.set)
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
studentDatabase.heading(3, text="Sex")
studentDatabase.column(3,width=75)
studentDatabase.heading(4, text="ID Number")
studentDatabase.column(4,width=100)
studentDatabase.heading(5, text="Year Level")
studentDatabase.column(5,width=70)
studentDatabase.heading(6, text="Course Code")
studentDatabase.column(6,width=100)
studentDatabase.heading(7, text="Status")
studentDatabase.column(7,width=100)

# ------------------------------------- F U N C T I O N S ------------------------------------------------ #

studentDatabase_predefinedrows = ["Last Name", "First Name", "Sex", "Year Level", "ID Number", "Course Code"]

# Read the CSV file and add the data to the treeview widget
with open(r"C:\Users\Acer\OneDrive\Desktop\Student Information System\StudentList.csv") as student_file:
    reader = csv.reader(student_file)
    if not studentDatabase_predefinedrows:  # Check if CSV file is empty
        predefined_rows = ["Last Name", "First Name", "Gender", "Year Level", "ID Number", "Course Code"]
        studentDatabase.insert("", "end", values=predefined_rows)  # Insert predefined rows to treeview
    else:
        for row in reader: 
            studentDatabase.insert("", "end", values=row)

def home(): # function that leads the user to the main page / tab

    if addButtonMain.winfo_exists():
        addButtonMain.pack()
    if delButton.winfo_exists():
        delButton.pack()
    if editButton.winfo_exists():
        editButton.pack()
    if viewCoursesButton.winfo_exists():
        viewCoursesButton.pack()
    if exitButton.winfo_exists():
        exitButton.pack()
    
    # Adjust frames if they exist
    if optionsFrame.winfo_exists():
        optionsFrame.place(x=25, y=50, width=200, height=530)
    if databaseFrame.winfo_exists():
        databaseFrame.place(x=250, y=50, width=930, height=530)
    
    # Destroy unnecessary frames if they exist
    if 'addStudentFrame' in globals() and addStudentFrame.winfo_exists():
        addStudentFrame.destroy()
    if 'studentDetailsFrame' in globals() and studentDetailsFrame.winfo_exists():
        studentDetailsFrame.destroy()
    if 'viewCoursesFrame' in globals() and viewCoursesFrame.winfo_exists():
        viewCoursesFrame.destroy()
    if 'courseOptionsFrame' in globals() and courseOptionsFrame.winfo_exists():
        courseOptionsFrame.destroy()
    if 'courseDatabaseFrame' in globals() and courseDatabaseFrame.winfo_exists():
        courseDatabaseFrame.destroy()
    
    # Show root window
    root.deiconify()

        
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

        # Connect to the MySQL database
        student_db = mysql.connector.connect(user='username', password='password', host='localhost', database='studentDatabase')
        cursor = student_db.cursor()

        # Getting the Inputs
        lastName = lastName_entry.get().capitalize()
        firstName = firstName_entry.get().capitalize()
        sexualOrientation = sexualOrientation_combo.get()
        yearLevel = int(yearLevel_entry.get())
        idNum = idNum_entry.get().strip()
        courseCode = courseCode_combo.get()

        # Checks if any of the entry fields are blank or empty
        if not(lastName and firstName and sexualOrientation and yearLevel and idNum):
            messagebox.showerror("Error","All fields must be filled.")
            return

        # Validates the ID input
        if not re.match(r'^\d{4}-\d{4}$', idNum): # Check if the ID format is valid
            messagebox.showerror("Invalid ID Input", "Oops! Enter a valid ID (YYYY-NNNN format)")
            return

        # Validates the year level input
        if not (1 <= yearLevel <= 4): #checks if year level input is valid
            messagebox.showerror("Invalid Year Level Input", "Oops! Enter a valid year level (1 to 4 only)")
            return

        # Check if the ID already exists
        query = "SELECT * FROM students WHERE idNum = %s"
        cursor.execute(query, (idNum,))
        result = cursor.fetchone()
        if result:
            messagebox.showinfo("Student Duplicate","Student already exists in the list. No duplicates allowed.")
            return

        # If the student is not a duplicate, add them to the database
        status = "Enrolled" if courseCode else "Unenrolled"
        query = "INSERT INTO students (lastName, firstName, sexualOrientation, idNum, yearLevel, courseCode, status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (lastName, firstName, sexualOrientation, idNum, yearLevel, courseCode, status))
        student_db.commit()

        # Display success message and clear the form
        messagebox.showinfo("Student Added","New Student Added Successfully!")
        lastName_entry.delete(0, 'end')
        firstName_entry.delete(0, 'end')
        sexualOrientation_combo.set('')
        idNum_entry.delete(0, 'end')
        yearLevel_entry.delete(0, 'end')
        courseCode_combo.set('')

        # Close the database connection
        cursor.close()
        student_db.close()

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
    with open(r"C:\Users\Acer\OneDrive\Desktop\Student Information System\CourseList.csv") as course_file:
        reader = csv.reader(course_file)
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
    values = studentDatabase.item(selectedStudent)['values']
    if not selectedStudent: # this ensures that 
        messagebox.showerror("Error", "Please select a student to delete.")
        return
    
    confirm = messagebox.askyesnocancel("Confiriming Deletion", "Are you sure you want to delete this student?")
    if not confirm:
        return

    studentDatabase.delete(selectedStudent) # this enables the user to delete a selected item or student from the student database treeview

    with open(r"C:\Users\Acer\OneDrive\Desktop\Student Information System\StudentList.csv") as student_file:
        reader = csv.reader(student_file)
        students=list(reader)
    
    for student in students:
        if student[:2]==values[:2]:
            students.remove(student)
            break

    with open(r"C:\Users\Acer\OneDrive\Desktop\Student Information System\StudentList.csv", "w", newline='') as student_file:
        writer = csv.writer(student_file)
        for student in students:
             writer.writerow(student)


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

    # --------------------------------- L A B E L S  &  E N T R I E S ------------------------------------#
    Label(editStudent_window, text="Last Name: ").grid(row=0, column=0, padx=5, pady=5)
    lastName= Entry(editStudent_window)
    lastName.insert(0, currentValues[0])
    lastName.grid(row=0, column=1, padx=5, pady=5)
    
    Label(editStudent_window, text="First Name: ").grid(row=1, column=0, padx=5, pady=5)
    firstName = Entry(editStudent_window)
    firstName.insert(0, currentValues[1])
    firstName.grid(row=1, column=1, padx=5, pady=5)

    Label(editStudent_window,text="Sex: ").grid(row=2,column=0,padx=5,pady=5)
    sexualOrientation = ttk.Combobox(editStudent_window,values=["Male","Female"])
    sexualOrientation.set(currentValues[2])
    sexualOrientation.grid(row=2,column=1,padx=5,pady=5)

    Label(editStudent_window, text="ID Number: ").grid(row=4, column=0, padx=5, pady=5)
    idNum_entry = Entry(editStudent_window)
    idNum_entry.insert(0, currentValues[3])
    idNum_entry.grid(row=4, column=1, padx=5, pady=5)

    Label(editStudent_window, text="Year Level: ").grid(row=3, column=0, padx=5, pady=5)
    yearLevel_entry = Entry(editStudent_window)
    yearLevel_entry.insert(0, currentValues[4])
    yearLevel_entry.grid(row=3, column=1, padx=5, pady=5)


    courseCodes=[]
    with open(r"C:\Users\Acer\OneDrive\Desktop\Student Information System\CourseList.csv") as course_file:
        reader = csv.reader(course_file)
        for row in reader:
            courseCodes.append(row[0])

    Label(editStudent_window, text="Course Code: ").grid(row=5, column=0, padx=5, pady=5)
    courseCode_entry = ttk.Combobox(editStudent_window,values=courseCodes,state="readonly")
    courseCode_entry.set(currentValues[5])
    courseCode_entry.grid(row=5, column=1, padx=5, pady=5)

    
    # -------------------------------- F U N C T I O N --------------------------------#
    def saveChanges():

        updatedDetails = [

            lastName.get().capitalize(),
            firstName.get().capitalize(),
            sexualOrientation.get(),
            idNum_entry.get(),
            yearLevel_entry.get(),
            courseCode_entry.get(),
            "Enrolled" if courseCode_entry.get().lower() else "Unenrolled"

        ]

         # Validation for year level
        try:
            yearLevel = int(yearLevel_entry.get())
            if not (1 <= yearLevel <= 4):
                messagebox.showerror("Invalid Year Level", "Year level must be between 1 and 4.")
                return
        except ValueError:
            messagebox.showerror("Invalid Year Level", "Year level must be a valid integer.")
            return

        # Validation for ID number
        if not re.match(r'^\d{4}-\d{4}$', idNum_entry.get()):
            messagebox.showerror("Invalid ID Number", "ID number must be in YYYY-NNNN format.")
            return

        studentDatabase.item(selectedStudent,values=updatedDetails) # updates the student data in treeview

        with open(r"C:\Users\Acer\OneDrive\Desktop\Student Information System\StudentList.csv", "w", newline="") as student_file:
            writer = csv.writer(student_file)
            for child in studentDatabase.get_children():
                values = studentDatabase.item(child, "values")
                writer.writerow(values)

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

    # Validates the course code input if it exists or not
    with open('CourseList.csv', 'r') as course_file:
        reader = csv.reader(course_file) #reads the CourseList.csv file
        courses = [row[0] for row in reader]

    if courseCode_entry.get() in courses: #checks whether user input of the student's course is found from the course list (valid)
        print(f"Course Name: {courseCode_entry.get()}")
        return
    else: 
        if courseCode_entry.get() == '': #if course input is empty
            return ''
        else:
            messagebox.showerror("Unvailable Course!",'Course Not Available! Please try again.')   
            print ('Unenrolled')
            return
        
def clearHighlights():
# Removes the highlight tag from all students in the treeview
    for student in studentDatabase.get_children():
        studentDatabase.item(student, tags=()) # remove all tags from the student  

def searchStudent():
    
    clearHighlights()
    # Gets the input from the search entry
    searchInput = searchStudent_entry.get().strip()
    
    # If the search input is empty, shows an error message
    if not searchInput:
        messagebox.showerror("Error","Search input must not be empty.")
        return
    
    # Gets the selected column to search
    searchColumn = searchStudent_category.get()
    
    matchingStudents = []
    # Checks if the search input matches any value in the selected column of the treeview
    for student in studentDatabase.get_children():
        if searchColumn == "Last Name":
            lastName = studentDatabase.set(student, 1) # makes sure that it only detects items within that certain column
            if searchInput.lower() in lastName.lower():
                matchingStudents.append(student) # add the student to the list of matching students
        elif searchColumn == "ID Number":
            idNum = studentDatabase.set(student, 4)
            if searchInput.lower() in idNum:
                studentDatabase.tag_configure('highlight', background='yellow') # selects the student with the matching search input
                studentDatabase.item(student, tags=('highlight'))
                studentDatabase.see(student) # brings the matching student into view
                break
    if matchingStudents: # if there are any matching students
        for student in matchingStudents:
            studentDatabase.tag_configure('highlight', background='yellow')
            studentDatabase.item(student, tags=('highlight'))
            studentDatabase.see(student)
    else:
        messagebox.showinfo("Student not found","Oops! Student not found in the list.")

############################################################
def viewCoursesPage():

# ------------ F R A M E S ------------------------------------------------ #
    global viewCoursesFrame
    viewCoursesFrame = ttk.Frame()
    
    global courseDatabaseFrame
    courseDatabaseFrame = ttk.Frame(root,relief=GROOVE,borderwidth=5)
    courseDatabaseFrame.place(x=25,y=50,width=1155,height=450)

    global courseOptionsFrame
    courseOptionsFrame = ttk.Frame(root,relief=GROOVE,borderwidth=5)
    courseOptionsFrame.place(x=25,y=500,width=1155,height=80)

# ---------------------------- C O U R S E  D A T A B A S E --------------- #
    global courseDatabase
    courseDatabase = ttk.Treeview(courseDatabaseFrame, columns=(1, 2), show="headings")
    courseDatabase.heading(1, text="Course Code")
    courseDatabase.heading(2, text="Course Name")

    with open(r"C:\Users\Acer\OneDrive\Desktop\Student Information System\CourseList.csv") as course_file:
        reader = csv.reader(course_file)
        for row in reader:
            courseDatabase.insert("", "end", values=row)

    courseDatabase.pack(fill="both", expand=True)

# ---------------------------- F U N C T I O N S ------------------------- #
    def addCourse():

        # ----------------- F U N C T I O N S ----------------------------- #
        def saveCourse():

            newCourseCode = addCourseCode.get().upper()
            newCourseName = addCourseName.get().upper()

            if not newCourseCode or not newCourseName:
                messagebox.showerror("Error", "Please fill in both Course Code and Course Name fields.")
                return

            with open(r"C:\Users\Acer\OneDrive\Desktop\Student Information System\CourseList.csv") as course_file: #read existing courses in csv file to check for any duplicates before adding new course
                reader = csv.reader(course_file)
                courses = [row for row in reader]

            if [newCourseCode,newCourseName] not in courses:
                courseDatabase.insert("","end",values=(newCourseCode,newCourseName)) #displays the newly added course to treeview
                with open(r"C:\Users\Acer\OneDrive\Desktop\Student Information System\CourseList.csv", "a", newline='') as course_file: # writes the newly added course to the CourseList or CSV file
                    writer = csv.writer(course_file)
                    writer.writerow([newCourseCode,newCourseName])
                    messagebox.showinfo("Course Added","New Course Added Successfully!")
            else:
                messagebox.showinfo("Course Duplicate","Course already exists in the list. No duplicates allowed.")

            addCourse_window.destroy()


        def cancelChanges():
            addCourse_window.destroy()

        # Pop-Up Window for Adding a new Course
        addCourse_window = tk.Tk()
        addCourse_window.resizable(False,False)
        addCourse_window.title("Add New Course")
        addCourse_window.geometry("300x160")
        
        # ----------------- L A B E L S  &  E N T R I E S ----------------- #
        Label(addCourse_window, text="Add New Course Code: ").grid(row=0, column=0, padx=5, pady=5)
        addCourseCode = Entry(addCourse_window)
        addCourseCode.grid(row=0, column=1, padx=5, pady=5)
        Label(addCourse_window, text="Add New Course Name: ").grid(row=1, column=0, padx=5, pady=5)
        addCourseName = Entry(addCourse_window)
        addCourseName.grid(row=1, column=1, padx=5, pady=5)

        # ------------------------- B U T T O N S --------------------------- #
        cancelButton = Button( # CANCEL Button (for Edit Student Window)
        addCourse_window, 
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

        saveButton = Button( # SAVE Button (for Add Course Window)
            addCourse_window, 
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
            command=saveCourse)
        saveButton.grid(row=6, column=0, columnspan=2, padx=70, pady=10)


    def deleteCourse():

       selectedCourse = courseDatabase.selection()

       if not selectedCourse:
           messagebox.showerror("Error", "Please select a student to delete.")
           return
       
       confirm = messagebox.askyesnocancel("Confiriming Deletion", "Are you sure you want to delete this course")
       if not confirm:
            return

       # Get the course code of the selected course
       course_values = courseDatabase.item(selectedCourse, "values")
       course_code = course_values[0]

       # Delete the course from the treeview
       courseDatabase.delete(selectedCourse)

       # Remove the course from the CourseList.csv file
       with open(r"C:\Users\Acer\OneDrive\Desktop\Student Information System\CourseList.csv") as course_file:
            courses = list(csv.reader(course_file))

       with open(r"C:\Users\Acer\OneDrive\Desktop\Student Information System\CourseList.csv", "w", newline='') as course_file:
            writer = csv.writer(course_file)
            for course in courses:
                if course[0] != course_code:
                    writer.writerow(course)

       # Unenroll students who are enrolled in the deleted course
       with open(r"C:\Users\Acer\OneDrive\Desktop\Student Information System\StudentList.csv") as student_file:
            reader = csv.reader(student_file)
            students = list(reader)

       updatedStudents = []
       for student in students:
            if student[5] == course_code:  # Check if the student is enrolled in the deleted course
                student[5] = ''  # Unenroll the student
                student[6] = "Enrolled"  if student[5] else "Unenrolled"  # Update the student's enrollment status
            updatedStudents.append(student)

       # Write the updated student list back to the StudentList.csv file
       with open(r"C:\Users\Acer\OneDrive\Desktop\Student Information System\StudentList.csv", "w", newline='') as student_file:
            writer = csv.writer(student_file)
            for student in updatedStudents:
                writer.writerow(student)

       messagebox.showinfo("Course Deleted", "Course deleted successfully!")


    def editCourse():

        selectedCourse = courseDatabase.selection()
        if not selectedCourse:
            messagebox.showerror("Error", "Please select a course to edit.")
            return
    
        # Get the selected student's current information
        currentCourseDetails = courseDatabase.item(selectedCourse, "values")

        # Pop-Up Window for Editing Course Details
        editCourse_window = tk.Tk()
        editCourse_window.resizable(False,False)
        editCourse_window.title("Edit Course")
        editCourse_window.geometry("300x280")

        # --------------------------------- L A B E L S  &  E N T R I E S ------------------------------------#
        Label(editCourse_window, text="Course Code: ").grid(row=0, column=0, padx=5, pady=5)
        courseCode= Entry(editCourse_window)
        courseCode.insert(0, currentCourseDetails[0])
        courseCode.grid(row=0, column=1, padx=5, pady=5)
        
        Label(editCourse_window, text="Course Name: ").grid(row=1, column=0, padx=5, pady=5)
        courseName = Entry(editCourse_window)
        courseName.insert(0, currentCourseDetails[1])
        courseName.grid(row=1, column=1, padx=5, pady=5)

        # -------------------------------- F U N C T I O N --------------------------------#
        def saveCourseChanges():

            updatedDetails = [

                courseCode.get().upper(),
                courseName.get().upper(),
            ]

            courseDatabase.item(selectedCourse,values=updatedDetails) # updates the course data in treeview

            with open(r"C:\Users\Acer\OneDrive\Desktop\Student Information System\CourseList.csv", "w", newline="") as course_file:
                writer = csv.writer(course_file)
                for child in courseDatabase.get_children():
                    values = courseDatabase.item(child, "values")
                    writer.writerow(values)

            messagebox.showinfo("Edit Student Success", "Student information updated successfully!")
            editCourse_window.destroy()

        def cancelChanges():

             editCourse_window.destroy()

        # ------------------------------- B U T T O N ----------------------------------- #
        
        saveButton = Button( # SAVE Button (for Edit Student Window)
        editCourse_window, 
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
        command=saveCourseChanges)
        saveButton.grid(row=6, column=0, columnspan=2, padx=70, pady=10)

        cancelButton = Button( # CANCEL Button (for Edit Student Window)
        editCourse_window, 
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
        font=('Arial', 12, 'bold'),
        command=addCourse)
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
        font=('Arial', 12, 'bold'),
        command=editCourse)
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

    viewCoursesFrame.pack()
    optionsFrame.pack_forget()
    databaseFrame.pack_forget()

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
    font=('Arial', 13, 'bold'),
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
    font=('Arial', 13, 'bold'),
    command=deleteStudent)
delButton.pack(pady=15)

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
    font=('Arial', 13, 'bold'),
    command=editStudent)
editButton.pack(pady=15)

Label(optionsFrame, text="Search by:").pack(pady=10)
searchStudent_category = ttk.Combobox(optionsFrame,values=["Last Name","ID Number"])
searchStudent_category.pack(pady=5)
searchStudent_entry=Entry(optionsFrame)
searchStudent_entry.pack(pady=5)

searchStudentButton = Button( # EDIT Button
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
    text = "SEARCH",
    font=('Arial', 9, 'bold'),
    command=searchStudent)
searchStudentButton.pack(pady=5)

clearSearchButton = Button( # CLEAR Button
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
    text = "CLEAR",
    font=('Arial', 9, 'bold'),
    command=clearHighlights)
clearSearchButton.pack(pady=5)

viewCoursesButton = Button( # EDIT Button
    optionsFrame, 
    background='BLUE',
    foreground='WHITE',
    activebackground='DARK CYAN',
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