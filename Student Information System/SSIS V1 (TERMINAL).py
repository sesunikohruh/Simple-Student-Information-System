import csv
import sys

class functions:

    def addStudent(): #this function adds the neccessary information of the student by asking the user for input

        predefined_rows = ["Last Name", "First Name", "ID Number", "Gender", "Year Level", "Course Code"] #code that adds the field names in csv file when the csv file is empty
        with open("StudentList.csv", "r") as student_file:
            reader = csv.reader(student_file)
            if predefined_rows != next(reader):
                with open("StudentList.csv", "w", newline="") as student_file:
                    writer = csv.writer(student_file)
                    writer.writerow(predefined_rows)

        lastName = input("\nLast Name: ")
        firstName = input("First Name: ")
        gender = input("Sex (M or F): ")

        while True:
            try:
                yearLevel = int(input("Year Level: "))
                if 1 <= yearLevel <= 4: #checks if year level input is valid
                    break
                else:
                    print("Oops! Enter a valid year level (1 to 4 only)")
            except ValueError:
                print("Oops! Enter a valid year level (1 to 4 only)")     

        idNum = input("ID Number: ")
                
        
        while True:

            courseCode = input("Course Code ").upper()
            with open('CourseList.csv', 'r') as course_file:
                reader = csv.reader(course_file) #reads the CourseList.csv file
                courses = [row[0] for row in reader]

            if courseCode in courses: #checks whether user input of the student's course is found from the course list (valid)
                print(f"Course Name: {courses[0]}")
                break #exits the loop once the course is found from the CourseList.csv file
            elif courseCode == '': #if course input is empty
                print ('N/A or Unenrolled')
                break
            else:
                print ('Course Not Available! Please try again.')
        
        with open("StudentList.csv", "r") as student_file: #checks for any duplicates before adding the student
                reader = csv.reader(student_file)
                students = [row for row in reader]

        if [lastName,firstName,idNum,gender,str(yearLevel),courseCode] not in student_file:
            with open("StudentList.csv", "a", newline='') as student_file:
                writer = csv.writer(student_file)
                writer.writerow([lastName,firstName,gender,idNum,yearLevel,courseCode])
                print("\nStudent added successfully!")
        else:
            print("Student already exists in the list. No duplicates allowed.")

    def displayStudent(): #this function lets the user view the list of students existing in the student list or database
        with open('StudentList.csv','r') as student_file:
            reader = csv.reader(student_file)
            #next(reader) #skips the header
            print("Last Name", "First Name", "ID Number", "Year Level", "Course")
            for row in reader:
                print(row)

    def editStudent(): #this function allows the user to make changes on specific details of a selected student or individual

        idNum = input("Enter the ID Number of the student you want to edit: ")
        with open('StudentList.csv','r') as student_file:
            reader = csv.reader(student_file)
            students = [row for row in reader]

        isStudentfound = False
        for i, student in enumerate(students):
            if student[2] == idNum:
                isStudentfound = True
                print("\nStudent found:")
                print("Last Name:", student[0])
                print("First Name:", student[1])
                print("ID Number:", student[2])
                print("Year Level:", student[3])
                print("Course:", student[4])

                lastName = input("\nEnter the new last name (press enter to keep the same): ").strip()
                if lastName:
                    students[i][0] = lastName

                firstName = input("Enter the new first name (press enter to keep the same): ").strip()
                if firstName:
                    students[i][1] = firstName

                while True:
                    yearLevelInput = input("Enter the new year level (press enter to keep the same): ").strip()
                    if yearLevelInput:
                        try:
                            yearLevel = int(yearLevelInput)
                            if 1 <= yearLevel <= 4:
                                students[i][3] = yearLevel
                                break
                            else:
                                print("Invalid year level. Must be between 1 and 4.")
                        except ValueError:
                            print("Invalid year level. Must be a number between 1 and 4.")
                    else:
                        break

                course = input("Enter the new course (press enter to keep the same): ").strip()
                if course:
                    with open('CourseList.csv', 'r') as course_file:
                        reader = csv.reader(course_file)
                        courses = [row[0] for row in reader]
                    if course not in courses:
                        print("Invalid course.")
                        break 
                    else:
                        students[i][4] = course

                print("\nLast Name: ", lastName)
                print("First Name: ", firstName)
                print("ID Number: ", idNum)
                print("Year Level: ", yearLevel)
                print("Course: ", course)
                print("\nSuccessfully Edited!")
                break

        if not isStudentfound:
            print("Student does not exist.")
        else:
            with open("StudentList.csv", "w", newline='') as student_file:
                writer = csv.writer(student_file)
                writer.writerows(students)

    def deleteStudent(): #this function enables the user to remove a selected student using its ID Number from the student list or database
        idNum_toDelete = input("Enter the ID Number of the student you want to delete: ")

        with open('StudentList.csv','r') as student_file:
            reader = csv.reader(student_file)
            students = [row for row in reader]

        for i, student in enumerate(students):
            if student[2] == idNum_toDelete:
                del students[i]
                break
        
        with open("StudentList.csv", "w", newline="") as student_file:
            writer = csv.writer(student_file)
            writer.writerows(students)
        
        print("Student deleted successfully!")

def main():

    while True:

        print("\nSTUDENT INFORMATION SYSTEM\n")

        menu = """        A. ADD STUDENT
        B. DISPLAY STUDENT LIST
        C. UPDATE/EDIT STUDENT DETAIL
        D. DELETE STUDENT
        E. EXIT   """

        print(menu)

        choice = (input("\nCHOOSE YOUR OPTION: ").upper())

        if choice == 'A':
            while True:
                functions.addStudent()
                addAnotherOpt = input("\nAdd another student? (Press Y for Yes and N for No): ")
                if addAnotherOpt == 'Y' and len(addAnotherOpt) == 1:
                    continue #goes back to beginning of the loop
                elif addAnotherOpt != 'Y' and len(addAnotherOpt) == 1: 
                    break #goes back to main menu
                else:
                     print("\nError choice! Input only Y or N to either proceed or not. Please try again.\n")
                     addAnotherOpt = input("\nAdd another student? (Press Y for Yes and N for No): ")
                     continue

        elif choice == 'B': #this option displays the student list
            while True:
                functions.displayStudent()
                break
        elif choice == 'C': #this option updates/edits chosen student detail
            while True:
                functions.editStudent()
                break
        elif choice == 'D': #this option deletes a chosen student information
            while True:
                functions.deleteStudent()
                break
        elif choice == 'E': #this option exits the program
            print("Exiting...")
            sys.exit()
        if choice not in ['A', 'B', 'C', 'D', 'E']:
            print("Invalid option! Please only choose from A to E\n") 
            print(menu)
            choice = (input("\nCHOOSE YOUR OPTION: ").upper())

if __name__ == "__main__":
        main()
        