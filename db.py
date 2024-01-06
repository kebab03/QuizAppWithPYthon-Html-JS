import sqlite3

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
import urllib

from sqlalchemy import create_engine, MetaData

# Replace your existing database connection setup with SQLite
engine = create_engine('sqlite:///your_database.db', echo=True)  # Replace 'path_to_your_database.db' with your desired database file
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# Create events table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        FName TEXT,
        LName TEXT,
        UName TEXT,
        Email TEXT,
        Password TEXT,
        role TEXT
    )
''')


cursor.execute('''
    CREATE TABLE IF NOT EXISTS course (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        course TEXT,
        userId INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS student_interest (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER ,
        student_interest TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS t_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT,
        course_id INTEGER,
        quiz_id INTEGER,
        user_id INTEGER
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS t_answers (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
        answer TEXT,
        quiz_id INTEGER,
        correct_ans TEXT,
        q_id INTEGER,
        user_id INTEGER
      
    )
''')



cursor.execute('''
    CREATE TABLE IF NOT EXISTS QuizNames (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
        quiz_name TEXT,
        course_id INTEGER,
        user_id INTEGER

    )
''')
conn.commit()

metadata = MetaData()

metadata.reflect(engine)

courseadd = metadata.tables["course"]

usersData = metadata.tables["Users"]

################################

# quiz_questions = metadata.tables["Questions"]

# quiz_options = metadata.tables["options"]

# quiz_answers = metadata.tables["answers"]

#######################

questions = metadata.tables['t_questions']



answers =  metadata.tables['t_answers']

quiznames = metadata.tables['QuizNames']

studentcourses = metadata.tables['student_interest']


Sessionlocal = scoped_session(
    sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False))
