import datetime
import database

menu = """Please select one of the following options:
1) Add new subject.
2) #### 
3) View all subjects
4) Add score of student
5) View scores for student.
6) Add student to the app.
7) Search for a subject.
8) Exit.
9) Search student using roll number
10) Update Score
11) Update Status
12) Update Student name using rollno
13) Update Student batch using rollno 
14) Filter students of a particular batch


Your selection: """
welcome = "Welcome to the STUDENT RESULT MANAGEMENT INTERFACE!"


def prompt_add_subject():
    title = input("Subject Name: ")
    database.add_subject(title)

def print_subjects_list(heading, subjects, flag):
    print(f"-- {heading} subjects --")
    for subject in subjects:
        if flag==0:
            print(f"{subject[0]}: {subject[1]}")
        elif flag == 2:
            print(f"{subject[0]}: {subject[1]}: {subject[2]}: {subject[3]}: {subject[4]}")
        elif flag == 3:
            print(f"{subject[0]}: {subject[1]}: {subject[2]}")
        else:
            print(f"{subject[0]}: {subject[1]}: {subject[3]}: {subject[4]}")
    print("---- \n")


def prompt_add_score_student():
    student_rollno = int(input("Roll Number: "))
    subject_id = input("Subject ID: ")
    marks = int(input("Marks: "))
    # status = int(input("Enter 1 for PASS and 0 for FAIL: "))
    database.add_score_subject(student_rollno, subject_id, marks, 0)#, status)


def prompt_get_score_all_subjects():
    rollno = input("Roll Number: ")
    return database.get_scores_student(rollno)


def prompt_add_student():
    rollno = int(input("Roll Number: "))
    name = input("Name: ")
    batch = input("Batch: ")
    database.add_student(rollno, name, batch)


def prompt_search_subject():
    search_term = input("Enter partial subject title: ")
    return database.search_subject(search_term)

def prompt_student_rollno():
    search_term = input("Enter student's roll number: ")
    return database.search_student_rollno(search_term)

def prompt_update_score():
    rollno = int(input("Enter student's roll number: "))
    subject_id = input("Enter Subject ID: ")
    new_marks = int(input("Enter new marks of student: "))
    return database.update_score(new_marks, rollno, subject_id)

def prompt_update_status():
    rollno = int(input("Enter student's roll number: "))
    subject_id = input("Enter Subject ID: ")
    new_status = int(input("Enter 1 for PASS and 0 for FAIL: "))
    return database.update_status(new_status, rollno, subject_id)

def prompt_update_student_name():
    rollno = int(input("Enter student's roll number: "))
    name = input("Enter correct name: ")
    return database.update_student_name(name, rollno)

def prompt_update_student_batch():
    rollno = int(input("Enter student's roll number: "))
    batch = input("Enter correct batch: ")
    return database.update_student_batch(batch, rollno)

def prompt_search_student_batch():
    batch = input("Enter batch: ")
    return database.search_student_batch(batch)

print(welcome)
database.create_tables()

while (user_input := int(input(menu))) != 8:
    if user_input == 1:
        prompt_add_subject()
    elif user_input == 3:
        subjects = database.get_subjects()
        print_subjects_list("All", subjects, 0)
    elif user_input == 4:
        prompt_add_score_student()
    elif user_input == 5:
        subjects = prompt_get_score_all_subjects()
        if subjects:
            print_subjects_list("Scores in", subjects, 1)
        else:
            print("Student has not been graded yet!")
    elif user_input == 6:
        prompt_add_student()
    elif user_input == 7:
        subjects = prompt_search_subject()
        if subjects:
            print_subjects_list("Subject(s) found", subjects, 0)
        else:
            print("Found no subjects for that search term!")
    elif user_input == 9:
        students = prompt_student_rollno()
        if students:
            print_subjects_list("Student found", students, 2)
        else:
            print("Sorry! No matching results found!")
    elif user_input == 10:
        updated_record = prompt_update_score()
        if updated_record:
            print_subjects_list("Student found", updated_record, 2)
        else:
            print("Sorry! Couldn't complete request. Kindly recheck rollno and Subject ID.")
    elif user_input == 11:
        updated_record = prompt_update_status()
        if updated_record:
            print_subjects_list("Student found", updated_record, 2)
        else:
            print("Sorry! Couldn't complete request. Kindly recheck rollno and Subject ID.")
    elif user_input == 12:
        updated_record = prompt_update_student_name()
        if updated_record:
            print_subjects_list("Scores in", updated_record, 3)
        else:
            print("No record exists for that rollno!")
    elif user_input == 13:
        updated_record = prompt_update_student_batch()
        if updated_record:
            print_subjects_list("Scores in", updated_record, 3)
        else:
            print("No record exists for that rollno!")
    elif user_input == 14:
        records = prompt_search_student_batch()
        if records:
            print_subjects_list("Scores in", records, 3)
        else:
            print("Nothing found!")
    else:
        print("Invalid input, please try again!")
