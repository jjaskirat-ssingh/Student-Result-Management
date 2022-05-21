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
    FOREIGN KEY(student_rollno) REFERENCES students(rollno) ON DELETE CASCADE,
    FOREIGN KEY(subject_id) REFERENCES subjects(id) ON DELETE CASCADE
);"""

INSERT_SUBJECT = "INSERT INTO subjects (name) VALUES (%s)"
SELECT_ALL_SUBJECTS = "SELECT * FROM subjects;" 
SELECT_ALL_STUDENTS = "SELECT * FROM students;" 
INSERT_STUDENT = "INSERT INTO students (rollno, name, batch) VALUES (%s, %s, %s)"
INSERT_MARKS_SUBJECT = "INSERT INTO scores (student_rollno, subject_id, marks, status) VALUES (%s, %s, %s, %s)"
SELECT_MARKS_STUDENT = """SELECT scores.*
FROM students
JOIN scores ON students.rollno = scores.student_rollno
JOIN subjects ON scores.subject_id = subjects.id
WHERE students.rollno = %s;"""
SEARCH_SUBJECT = """SELECT * FROM subjects WHERE name LIKE %s;"""

SEARCH_STUDENT_ROLLNO = """

CREATE OR REPLACE FUNCTION SEARCH_STUDENT_ROLLNO_(roll integer)
RETURNS TABLE(auxname TEXT, auxbatch TEXT, auxsubname TEXT, auxmarks INTEGER, auxstatus INTEGER)
-- RETURNS setof my_type 
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
    -- into ret.auxname, ret.auxbatch, ret.auxsubname, ret.auxmarks, ret.auxstatus
    from (students s join scores sc on s.rollno = sc.student_rollno) join subjects sub on sub.id = sc.subject_id
    where s.rollno = roll;
    -- RETURN ret;
    -- RETURN NEXT;
end; 
$$
LANGUAGE plpgsql;
"""

FILTER_BY_SUBJECT = """

CREATE OR REPLACE FUNCTION FILTER_BY_SUBJECT(subid integer)
RETURNS TABLE(auxrollno INTEGER, auxname TEXT, auxbatch TEXT, auxsubname TEXT, auxmarks INTEGER, auxstatus INTEGER)
-- RETURNS setof my_type 
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
    select s.rollno, s.name, s.batch, sub.name, sc.marks, sc.status
    -- into ret.auxname, ret.auxbatch, ret.auxsubname, ret.auxmarks, ret.auxstatus
    from (students s join scores sc on s.rollno = sc.student_rollno) join subjects sub on sub.id = sc.subject_id
    where sub.id = subid;
    -- RETURN ret;
    -- RETURN NEXT;
end; 
$$
LANGUAGE plpgsql;
"""
############################################################################

# SEARCH_STUDENT_ROLLNO_CALL = """
#     call SEARCH_STUDENT_ROLLNO(rollno);
# """

STATUS_UPDATE_TRIGGER_FUNCTION = """
create or replace function update_status_func()
	returns trigger
	language plpgsql
	as 
$$
begin
	if NEW.marks > 33 then
		update score set status = 1;
	end if;
	return new
end
$$
"""

# # create trigger status_update
# # 	after update
# # 	on scores
# # 	for each row
# # 	execute procedure update_status_func();
# # $$
# # """
# # CREATE FUNCTION getSomeData()
# # RETURNS trigger
# # AS $$
# # begin
# # import subprocess
# # subprocess.call(['/path/to/your/virtual/environment/bin/python3', '/some_folder/some_sub_folder/get_data.py'])
# # end;
# # $$
# # LANGUAGE plpythonu;

STATUS_UPDATE_TRIGGER = """
CREATE FUNCTION STATUS_UPDATE_TRIGGER
RETURNS TRIGGER 
AS $$
BEGIN
  after update, insert
  ON scores
  for each row
  execute function update_status_func();
END;
$$
LANGUAGE plpgsql;
"""

############################################################################

UPDATE_SCORE = """
--To update score

CREATE OR REPLACE function UPDATE_SCORE(new_mark INTEGER, roll INTEGER, sub INTEGER) 
RETURNS void  
AS 
$$ 
DECLARE 
    --ret record;
BEGIN
    UPDATE scores 
    SET marks=UPDATE_SCORE.new_mark 
    WHERE student_rollno=UPDATE_SCORE.roll AND subject_id=UPDATE_SCORE.sub; 
    --RETURNING *;

    --SELECT s.name, s.batch, sub.name, sc.marks, sc.status
    --INTO ret.name, ret.batch, ret.sub_name, ret.marks, ret.status
    --INTO ret
    --from (students s join scores sc on s.rollno = sc.student_rollno)
    --    join subjects sub on sc.subject_id = sub.id
    --    where s.rollno = roll and sub.subject_id=sub;
    --return ret;
END;
$$ 
language plpgsql;
"""

UPDATE_STATUS = """
CREATE OR REPLACE FUNCTION UPDATE_STATUS(new_status integer, roll integer, sub integer)
RETURNS VOID AS 
$$
BEGIN
    UPDATE scores 
    SET status = new_status 
    WHERE student_rollno = roll and subject_id = sub;
END;
$$
LANGUAGE PLPGSQL
"""

UPDATE_STUDENT_NAME = """
CREATE OR REPLACE FUNCTION UPDATE_STUDENT_NAME(new_name TEXT, roll INTEGER)
RETURNS TABLE(auxrollno INTEGER, auxname TEXT, auxbatch TEXT) AS
$$
DECLARE 
    --ret RECORD;
BEGIN
    UPDATE students 
    SET name = new_name 
    WHERE rollno = roll;

    RETURN QUERY
    SELECT * FROM students 
    --INTO ret
    WHERE rollno = roll;
    --return ret;
END;
$$
LANGUAGE PLPGSQL
"""

UPDATE_STUDENT_BATCH = """
CREATE OR REPLACE FUNCTION UPDATE_STUDENT_BATCH(new_batch TEXT, roll INTEGER)
RETURNS TABLE(auxrollno INTEGER, auxname TEXT, auxbatch TEXT) AS
$$
DECLARE 
    --ret RECORD;
BEGIN
    UPDATE students 
    SET batch = new_batch 
    WHERE rollno = roll;

    RETURN QUERY
    SELECT * FROM students 
    --INTO ret
    WHERE rollno = roll;
    --return ret;
END;
$$
LANGUAGE PLPGSQL
"""

SEARCH_STUDENT_BATCH = """
CREATE OR REPLACE FUNCTION SEARCH_STUDENT_BATCH(batch_no varchar)
-- returns table(auxname TEXT, auxbatch TEXT, auxsubname TEXT, auxmarks INTEGER, auxstatus INTEGER)
-- returns SETOF RECORD
returns table(auxrollno INTEGER, auxname TEXT, auxbatch TEXT)
AS 
$$
DECLARE 
    -- ret record;
    -- Cursor
    -- entries CURSOR FOR SELECT * from students ORDER BY batch;
BEGIN
    RETURN QUERY
    SELECT * FROM students where batch = batch_no;
    -- OPEN entries;

    -- LOOP
    -- fetch entries into ret;
    --     exit when ret = null;
    --     if ret.batch  = batch_no then
    --         return next ret;
    --     end if;
    -- END LOOP;  
    
    -- CLOSE entries;
END;
$$ LANGUAGE plpgsql
"""

# SEARCH_STUDENT_BATCH = """
# CREATE OR REPLACE FUNCTION SEARCH_STUDENT_BATCH(batchno TEXT)
# RETURNS refcursor AS '
# DECLARE 
#     ref refcursor;
#     --entries CURSOR FOR
#     --   SELECT * FROM students WHERE batch = batchno;
# BEGIN 
#     OPEN ref for SELECT * FROM students WHERE batch = batchno;
 
#     LOOP
#     FETCH entries into ref;
#         EXIT WHEN ref = NULL;
#         return NEXT ref;
#     END LOOP;
#     --CLOSE entries;
#     return ref;
# END;
# '
# LANGUAGE plpgsql
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
            

def drop_tables():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("""DROP TABLE IF EXISTS students, subjects, scores""")
            # cursor.execute(CREATE_STUDENTS_TABLE)
            # cursor.execute(CREATE_SCORES_TABLE)


def add_subject(name):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_SUBJECT, (name,))

def get_subjects():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_SUBJECTS)
            return cursor.fetchall()

def get_students():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SELECT_ALL_STUDENTS)
            return cursor.fetchall()

def add_student(rollno, name, batch):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_STUDENT, (rollno, name, batch))

def add_score_subject(student_rollno, subject_id, marks, status):
    with connection:
        with connection.cursor() as cursor:
            # cursor.execute(STATUS_UPDATE_TRIGGER)
            # cursor.execute(STATUS_UPDATE_TRIGGER_FUNCTION)
            
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
        
def filter_by_subject(subid):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(FILTER_BY_SUBJECT, (subid,))
            cursor.execute("SELECT * FROM FILTER_BY_SUBJECT( %s); ", (subid,))
            return cursor.fetchall()

def update_score(new_marks, rollno, subject):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_SCORE, (new_marks, rollno, subject))
            cursor.execute("SELECT FROM UPDATE_SCORE(%s, %s, %s); ", (new_marks, rollno, subject))
            cursor.execute(SEARCH_STUDENT_ROLLNO, (rollno,))
            cursor.execute("SELECT * FROM SEARCH_STUDENT_ROLLNO_( %s); ", (rollno,))
            return cursor.fetchall()

def update_status(new_status, rollno, subject):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_STATUS, (new_status, rollno, subject))
            cursor.execute("SELECT FROM UPDATE_STATUS(%s, %s, %s); ", (new_status, rollno, subject))
            cursor.execute(SEARCH_STUDENT_ROLLNO, (rollno,))
            cursor.execute("SELECT * FROM SEARCH_STUDENT_ROLLNO_( %s); ", (rollno,))
            return cursor.fetchall()

def update_student_name(name, rollno):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_STUDENT_NAME, (name, rollno))
            cursor.execute("SELECT * FROM UPDATE_STUDENT_NAME(%s, %s)", (name, rollno))
            return cursor.fetchall()

def update_student_batch(batch, rollno):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(UPDATE_STUDENT_BATCH, (batch, rollno))
            cursor.execute("SELECT * FROM UPDATE_STUDENT_BATCH(%s, %s)", (batch, rollno))
            return cursor.fetchall()

def search_student_batch(batch):
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(SEARCH_STUDENT_BATCH, (batch,))
            cursor.execute("SELECT * FROM SEARCH_STUDENT_BATCH(%s); ", (batch,))
            rows = cursor.fetchall()
            return rows
        
def delete_student_name(name) :
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_STUDENT_NAME, (name,))
            return cursor.fetchall()

DELETE_STUDENT_NAME = """DELETE FROM students where name = (%s);
                         SELECT * FROM students;"""
                         
        
def delete_student_roll(name) :
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_STUDENT_ROLL, (name,))
            return cursor.fetchall()

DELETE_STUDENT_ROLL = """DELETE FROM students where rollno = (%s);
                         SELECT * FROM students;"""

        
def delete_subject(name) :
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_SUBJECT, (name,))
            return cursor.fetchall()

DELETE_SUBJECT = """DELETE FROM subjects where name = (%s);
                         SELECT * FROM subjects;"""