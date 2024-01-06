from logging import error
from db import Sessionlocal
from db import metadata
from db import usersData
from db import courseadd
from sqlalchemy import insert, delete, update, and_
from utils import passwordhashing
from sqlalchemy import select
from flask import session
from sqlalchemy.sql import text
from logzero import logger
from db import answers
from db import questions
from db import quiznames
from db import studentcourses
from sqlalchemy import join
from sqlalchemy.sql import select





def createUser(fname, lname, uname, email, password, role):

    try:

        # --------Create User--------
        db = Sessionlocal
        print("--------------------------------------")
        print(fname, lname, uname, email, password, role)
        print("--------------***********************************------------------------")
        convertedpassword = passwordhashing(password)

        insertuser = insert(usersData).values(FName=fname, LName=lname,
                                              UName=uname, Email=email, Password=convertedpassword, role=role)

        db.execute(insertuser)

# -----------To get Student Id -----

        result = db.query(usersData).filter(usersData.c.Email == email).first()

        print(" result===================================== {}.  ".format(result))
        name = "Alice"
        age = 30
        print(" my name is {}. I am {} years old".format(name, age))
        print("type of result ----",type(result))
        print("type of result ----*****=", result.role)
        session['St_ID'] = result.Id

        logger.info("Student_ID {}".format(session['St_ID']))

# -----------------------------------

        db.commit()
        db.close()

    except:
        db.rollback()
        db.close()
        raise Exception

#-------------------------------------------------------------------------------------------------

def checkUser(usn, psw):

    try:

        db = Sessionlocal

        psw = passwordhashing(psw)
        print(f" user name :=  {usn} and Passwor is:-- {psw}")
        result = db.query(usersData).filter(
            and_(usersData.c.Email == usn, usersData.c.Password == psw)).first()

        session['UID'] = result.Id

        if result:
            return result
        else:
            return False

    except:

        db.rollback()

#-------------------------------------------------------------------------------------------------

def getuserrole(uid):

    try:

        db = Sessionlocal

        result = db.query(usersData).filter(usersData.c.Id == uid).first()

        return result.role

    except Exception as e:

        logger.error(e)

#-------------------------------------------------------------------------------------------------

def addcourse(course):
    try:

        db = Sessionlocal

        insertcourse = insert(courseadd).values(
            userId=session.get('UID'), course=course)

        db.execute(insertcourse)
        db.commit()
        db.close()

    except:

        db.rollback()
        db.close()
        raise Exception

#-------------------------------------------------------------------------------------------------

def insertcourse(course_Names):
    try:

        db = Sessionlocal

        for i in range(len(course_Names)):

            student_course = insert(studentcourses).values(
                user_id=session.get('St_ID'), student_interest=course_Names[i])

            db.execute(student_course)

        db.commit()
        db.close()

    except:

        db.rollback()
        db.close()
        raise Exception

#-------------------------------------------------------------------------------------------------

def insertcourseafterlogin(course_Names):
    try:

        db = Sessionlocal

        for i in range(len(course_Names)):
            print(f"session.get(=====   line 154 :: {session.get('UID')}")
            student_course = insert(studentcourses).values(
                user_id=session.get('UID'), student_interest=course_Names[i])

            db.execute(student_course)

        db.commit()
        db.close()

    except:

        db.rollback()
        db.close()
        raise Exception

#-------------------------------------------------------------------------------------------------

def getcourse():
    print(f"session.get(=====   line 172  crud  :: {session.get('UID')}")
    try:

        db = Sessionlocal
        print (" line ---------------- 173 --******   crud .py")
        result = db.query(courseadd).filter(
            courseadd.c.userId == session.get('UID')).all()

        logger.info(str(result))
        return result

    except Exception as e:

        logger.error(e)

#-------------------------------------------------------------------------------------------------

def getcoursesdropdown():
    print(f"session.get(=====   line 190 crud :: {session.get('UID')}")
    try:

        db = Sessionlocal

        result = db.query(courseadd, studentcourses).filter(and_(
            courseadd.c.ID == studentcourses.c.student_interest, studentcourses.c.user_id == session.get('UID'))).all()

        logger.info(str(result))
        return result

    except Exception as e:

        logger.error(e)

#-------------------------------------------------------------------------------------------------

def getstudentcourse():

    db = Sessionlocal

    # result = db.query(studentcourses).filter(
    #     studentcourses.c.user_id == session.get('UID')).all()
    print(" crud line 210 courseadd.c.ID")

    print(" crud line 212 studentcourses.c.student_interest")
    print(" crud line 213 studentcourses.c.user_id ")

    result1 = db.query(courseadd, studentcourses).filter(and_(
        courseadd.c.ID == studentcourses.c.student_interest, studentcourses.c.user_id == session.get('UID'))).all()
    print(f" line 220  type of result1::::::::::::::------ {type(result1)}")
    print(f"result1::= {result1}")
    logger.info("result: {}".format(result1))

    return result1

#-------------------------------------------------------------------------------------------------

def getallcourses():

    try:

        db = Sessionlocal

        result = db.query(courseadd).all()
        print("235 crud.py of result----*****=", result)
        print(f" crud line 236  type of result===:::::::---- {type(result)}")
        print(f"result==::= {result}")
        logger.info(str(result))
        return result

    except Exception as e:

        logger.error(e)

#-------------------------------------------------------------------------------------------------

def insertQuestionandAnswer(ques, id,  options, ans, quiz_id):

    # -------insert question---------

    db = Sessionlocal
    insertquestion = insert(questions).values(
        question=ques, course_id=id, quiz_id=quiz_id, user_id=session.get('UID'))
    db.execute(insertquestion)

# ---------Search----------

    result = db.query(questions).filter(
        and_(questions.c.question == ques, questions.c.course_id == id)).first()
    Q_id = result.id

    for i in range(len(options)):

        insertoption = insert(answers).values(
            answer=options[i], correct_ans=ans[i], q_id=Q_id, quiz_id=quiz_id, user_id=session.get('UID'))

        db.execute(insertoption)

    db.commit()
    db.close()

#-------------------------------------------------------------------------------------------------

def getquizquestion(cid, qu_id):
    try:
        db = Sessionlocal

        result = db.query(questions).filter(and_(questions.c.user_id == session.get(
            'UID'), questions.c.course_id == cid, questions.c.quiz_id == qu_id)).all()

        logger.info("result {}".format(result))

        if result:

            qid = [i.id for i in result]

            logger.info("qid{}".format(qid))

            result1 = db.query(answers).filter(and_(answers.c.q_id.in_(
                qid), answers.c.user_id == session.get('UID'), answers.c.quiz_id == qu_id)).all()

            logger.info("result1 {}".format(result1))

            return (result, result1)

        else:
            return (None, None)

    except Exception as e:
        logger.info(e)

#-------------------------------------------------------------------------------------------------

def add_quiz(quiz_name, course_id):

    try:
        db = Sessionlocal

        insertquizname = insert(quiznames).values(
            quiz_name=quiz_name, course_id=course_id, user_id=session.get('UID'), )
        db.execute(insertquizname)

        db.commit()
        db.close()

    except Exception as e:
        logger.info(e)

#-------------------------------------------------------------------------------------------------

def get_Quiznames():

    try:
        print(f"line 324  session.get('UID') == {session.get('UID')}")
        db = Sessionlocal

        result = db.query(quiznames).filter(
            quiznames.c.user_id == session.get('UID')).all()

        logger.info(str(result))
        return result

    except Exception as e:

        logger.error(e)

#-------------------------------------------------------------------------------------------------

def get_QuiznamesStudent(cid):

    try:

        db = Sessionlocal

        result = db.query(quiznames).filter(quiznames.c.course_id == cid).all()

        logger.info(str(result))

        return result

    except Exception as e:

        logger.error(e)

#-------------------------------------------------------------------------------------------------

def studentQuizQuestions(qu_id, cid):
    try:
        print(f" line 359 crud py qu_id ={qu_id} cid ={cid}  ")
        db = Sessionlocal

        result = db.query(questions).filter(and_(questions.c.course_id == cid, questions.c.quiz_id == qu_id)).all()

        logger.info("result{}".format(result))

        if result:

            qes_id = [i.id for i in result]

            logger.info("qid{}".format(qes_id))

            result1 = db.query(answers).filter(answers.c.q_id.in_(qes_id)).all()
            print(f" line 374 crud py result1 ={result1}   ")
            logger.info(" 374 crud py result1 {}".format(result1))

            return (result, result1)

        else:
            return (None, None)
    
    except Exception as e:

        logger.error(e)





def get_question_count(courseid , quizid ):

    db = Sessionlocal

    result = db.query(questions).filter(and_(questions.c.course_id == courseid, questions.c.quiz_id == quizid)).all()
    print("  crud result line 394 ",result)
    if result:
        return len(result)

    return None




def get_question_id(courseid , quizid ):

    db = Sessionlocal
    print(f" line 406 in crud.py   quizid== {quizid} courseid=={courseid} ")
    result = db.query(questions).filter(and_(questions.c.course_id == courseid, questions.c.quiz_id == quizid)).all()
    print(f"crud py  line 408 resuet of query is :- {result}")
    if result:
        tryp=[str(i.id) for i in result]
        print(f" 411 type of tryp {type(tryp)}")
        print(f" 412 len of tryp {len(tryp)}")
        #return [str(i.id) for i in result]
        return tryp

    return None