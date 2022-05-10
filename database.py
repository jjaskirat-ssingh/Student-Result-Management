import os
import datetime
import psycopg2
from dotenv import load_dotenv
load_dotenv()

CREATE_SUBJECTS_TABLE = """CREATE TABLE IF NOT EXISTS subjects (
    id SERIAL PRIMARY KEY,
    name TEXT
);"""

CREATE_STUDENTS_TABLE = """CREATE TABLE IF NOT EXISTS students (
    username TEXT PRIMARY KEY
);"""

CREATE_SCORES_TABLE = """CREATE TABLE IF NOT EXISTS scores (
    student_username TEXT,
    subject_id INTEGER,
    marks INTEGER,
    FOREIGN KEY(student_username) REFERENCES students(username),
    FOREIGN KEY(subject_id) REFERENCES subjects(id)
);"""

INSERT_SUBJECT = "INSERT INTO subjects (name) VALUES (%s)"
SELECT_ALL_SUBJECTS = "SELECT * FROM subjects;"
INSERT_STUDENT = "INSERT INTO students (username) VALUES (%s)"
INSERT_MARKS_SUBJECT = "INSERT INTO scores (student_username, subject_id, marks) VALUES (%s, %s, %s)"
SELECT_MARKS_STUDENT = """SELECT scores.*
FROM students
JOIN scores ON students.username = scores.student_username
JOIN subjects ON scores.subject_id = subjects.id
WHERE students.username = %s;"""
SEARCH_SUBJECT = """SELECT * FROM subjects WHERE name LIKE %s;"""

dbname = os.environ.get("DATABASE_NAME")
user = os.environ.get("DATABASE_USER")
password = os.environ.get("DATABASE_PASSWORD")
y = "dbname=" + dbname + " user=" + user + " password=" + password
connection = psycopg2.connect(y)

def create_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(CREATE_SUBJECTS_TABLE)
            cursor.execute(CREATE_STUDENTS_TABLE)
            cursor.execute(CREATE_SCORES_TABLE)

def add_subject(name):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_SUBJECT, (name,))

def get_subjects(upcoming=False):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_SUBJECTS)
            return cursor.fetchall()

def add_student(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_STUDENT, (username,))

def add_score_subject(username, subject_id, marks):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MARKS_SUBJECT, (username, subject_id, marks))

def get_scores_student(username):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_MARKS_STUDENT, (username,))
            return cursor.fetchall()

def search_subject(search_term):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SEARCH_SUBJECT, (f"%{search_term}%",))
            return cursor.fetchall()