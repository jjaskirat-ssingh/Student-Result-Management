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
        else:
            print(f"{subject[0]}: {subject[1]}: {subject[2]}")
    print("---- \n")


def prompt_add_score_student():
    username = input("Username: ")
    subject_id = input("Subject ID: ")
    marks = int(input("Marks: "))
    database.add_score_subject(username, subject_id, marks)


def prompt_get_score_all_subjects():
    username = input("Username: ")
    return database.get_scores_student(username)


def prompt_add_student():
    username = input("Username: ")
    database.add_student(username)


def prompt_search_subject():
    search_term = input("Enter partial movie title: ")
    return database.search_subject(search_term)


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
            print_subjects_list("Subject(s) found", subjects)
        else:
            print("Found no subjects for that search term!")
    else:
        print("Invalid input, please try again!")
