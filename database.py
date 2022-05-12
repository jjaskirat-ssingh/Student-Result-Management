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
    rollno INTEGER PRIMARY KEY,
    name TEXT,
    batch TEXT
);"""

CREATE_SCORES_TABLE = """CREATE TABLE IF NOT EXISTS scores (
    score_id SERIAL PRIMARY KEY,
    student_rollno INTEGER,
    subject_id INTEGER,
    marks INTEGER,
    status INT CHECK (status=1 OR status=0), 
    FOREIGN KEY(student_rollno) REFERENCES students(rollno),
    FOREIGN KEY(subject_id) REFERENCES subjects(id)
);"""

INSERT_SUBJECT = "INSERT INTO subjects (name) VALUES (%s)"
SELECT_ALL_SUBJECTS = "SELECT * FROM subjects;" 
INSERT_STUDENT = "INSERT INTO students (rollno, name, batch) VALUES (%s, %s, %s)"
INSERT_MARKS_SUBJECT = "INSERT INTO scores (student_rollno, subject_id, marks, status) VALUES (%s, %s, %s, %s)"
SELECT_MARKS_STUDENT = """SELECT scores.*
FROM students
JOIN scores ON students.rollno = scores.student_rollno
JOIN subjects ON scores.subject_id = subjects.id
WHERE students.rollno = %s;"""
SEARCH_SUBJECT = """SELECT * FROM subjects WHERE name LIKE %s;"""

SEARCH_STUDENT_ROLLNO = """
DROP FUNCTION SEARCH_STUDENT_ROLLNO_(roll integer);
--DROP TYPE my_type;

--CREATE TYPE my_type AS (auxname TEXT, auxbatch TEXT, auxsubname TEXT, auxmarks INTEGER, auxstatus INTEGER);

CREATE OR REPLACE FUNCTION SEARCH_STUDENT_ROLLNO_(roll integer)
RETURNS TABLE(auxname TEXT, auxbatch TEXT, auxsubname TEXT, auxmarks INTEGER, auxstatus INTEGER)
--RETURNS setof my_type 
AS 
$$
declare
    --ret my_type;
    ret RECORD; 
    --auxname TEXT;
    --auxbatch TEXT;
    --auxsubname TEXT;
    --auxmarks INTEGER;
    --auxstatus INTEGER;
begin
    RETURN QUERY
    select s.name, s.batch, sub.name, sc.marks, sc.status
    --into ret.auxname, ret.auxbatch, ret.auxsubname, ret.auxmarks, ret.auxstatus
    from (students s join scores sc on s.rollno = sc.student_rollno) join subjects sub on sub.id = sc.subject_id
    where s.rollno = roll;
    --RETURN ret;
    --RETURN NEXT;
end; 
$$
LANGUAGE plpgsql;
"""

# SEARCH_STUDENT_ROLLNO_CALL = """
#     call SEARCH_STUDENT_ROLLNO(rollno);
# """

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

def get_subjects():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_SUBJECTS)
            return cursor.fetchall()

def add_student(rollno, name, batch):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_STUDENT, (rollno, name, batch))

def add_score_subject(student_rollno, subject_id, marks, status):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MARKS_SUBJECT, (student_rollno, subject_id, marks, status))

def get_scores_student(rollno):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_MARKS_STUDENT, (rollno,))
            return cursor.fetchall()

def search_subject(search_term):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SEARCH_SUBJECT, (f"%{search_term}%",))
            return cursor.fetchall()

def search_student_rollno(rollno):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SEARCH_STUDENT_ROLLNO, (rollno,))
            cursor.execute("SELECT * FROM SEARCH_STUDENT_ROLLNO_( %s); ", (rollno,))
            return cursor.fetchall()