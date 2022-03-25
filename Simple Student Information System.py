# Student Management System
"""
Fields :- ['Name', 'ID No.', 'Year Level', 'Gender', 'Course']
1. Add New Student
2. View Students
3. Search Student
4. Update Student
5. Delete Student
6. Quit
"""

import csv

# Define global variables
student_fields = ['Name', 'ID No.', 'Year Level', 'Gender', 'Course']
student_database = 'student data.csv'


def display_menu():
    print("--------------------------------------------------------")
    print("------Welcome to Simple Student Information System------")
    print("--------------------------------------------------------")
    print("1. Add New Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Update Student")
    print("5. Delete Student")
    print("6. Quit")


def add_student():
    print("-------------------------")
    print("Add Student Information")
    print("-------------------------")
    global student_fields
    global student_database

    student_data = []
    for field in student_fields:
        value = input("Enter " + field + ": ")
        student_data.append(value)

    with open(student_database, "a", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows([student_data])

    print("**Data saved successfully!**")
    input("**Press any key to continue.**")
    return


def view_students():
    global student_fields
    global student_database

    print("--- Student Records ---")

    with open(student_database, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for x in student_fields:
            print(x, end='\t |')
        print("\n-----------------------------------------------------------------")

        for row in reader:
            for item in row:
                print(item, end="\t |")
            print("\n")

    input("**Press any key to continue.**")


def search_student():
    global student_fields
    global student_database

    print("----------------------")
    print("--- Search Student ---")
    print("----------------------")
    idnum = input("Enter ID No. to search: ")
    with open(student_database, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) > 0:
                if idnum == row[1]:
                    print("-------------------------")
                    print("----- Student Found -----")
                    print("-------------------------")
                    print("Name: ", row[0])
                    print("ID No.: ", row[1])
                    print("Year Level: ", row[2])
                    print("Gender: ", row[3])
                    print("Course: ", row[4])
                    break
        else:
            print("**ID No. not found in our database!**")
    input("**Press any key to continue.**")


def update_student():
    global student_fields
    global student_database

    print("----------------------")
    print("--- Update Student ---")
    print("----------------------")
    idnum = input("Enter ID No. to update: ")
    index_student = None
    updated_data = []
    with open(student_database, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        counter = 0
        for row in reader:
            if len(row) > 0:
                if idnum == row[1]:
                    index_student = counter
                    print("Student Found: at index ", index_student)
                    student_data = []
                    for field in student_fields:
                        value = input("Enter " + field + ": ")
                        student_data.append(value)
                    updated_data.append(student_data)
                else:
                    updated_data.append(row)
                counter += 1

    # Check if the record is found or not
    if index_student is not None:
        with open(student_database, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(updated_data)
    else:
        print("**ID No. not found in our database!**")

    input("**Press any key to continue.**")


def delete_student():
    global student_fields
    global student_database

    print("----------------------")
    print("--- Delete Student ---")
    print("----------------------")
    idnum = input("Enter ID no. to delete: ")
    student_found = False
    updated_data = []
    with open(student_database, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        counter = 0
        for row in reader:
            if len(row) > 0:
                if idnum != row[1]:
                    updated_data.append(row)
                    counter += 1
                else:
                    student_found = True

    if student_found is True:
        with open(student_database, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerows(updated_data)
        print("**ID No. ", idnum, "deleted successfully!**")
    else:
        print("**ID No. not found in our database!**")

    input("**Press any key to continue.**")


while True:
    display_menu()

    choice = input("Enter your choice: ")
    if choice == '1':
        add_student()
    elif choice == '2':
        view_students()
    elif choice == '3':
        search_student()
    elif choice == '4':
        update_student()
    elif choice == '5':
        delete_student()
    else:
        break

print("-------------------------------")
print(" Thank you for using my system")
print("-------------------------------")
