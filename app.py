from flask import Flask, flash, render_template, request, url_for, redirect, session, abort
from logzero import logger
from sqlalchemy.sql.operators import op
import crud
import urllib
from db import courseadd
from functools import wraps
from flask import g


app = Flask(__name__)

app.secret_key = 'rohit'


def restricted(access_level):
    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):
            print(access_level)
            # uid = session.get("UID")
            user_id = session.get("UID")

            logger.warning("-----> user_id: {} st_id: {}".format(user_id))

            role = crud.getuserrole(user_id)

            if role:
                if role not in access_level:
                    abort(403)
            else:
                abort(404)

            return function(*args, **kwargs)

        return wrapper

    return decorator


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        get_UID = session.get('UID')
        logger.warning("get_UID: {}".format(get_UID))
        if not get_UID:

            return render_template('login.html')

        return f(*args, **kwargs)
    return decorated_function

# -------------------------------------------------------------------------------------------------


@app.route('/', methods=['GET'])
def main():
    return render_template('main.html')

# -------------------------------------------------------------------------------------------------


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template('login.html')

    else:
        usn = str(request.form.get('email'))
        psw = str(request.form.get('password'))

        logger.info("Username: {} Password: {}".format(usn, psw))

        error = None
        '''
        class Role:
            def __init__(self, role_name):
                self.role = role_name

            def __repr__(self):
                return f"Role(role_name='{self.role}')"

        # Creating instances of the Role class
        result = Role(role_name='student')
        role2 = Role(role_name='User')

        # Accessing attributes
        print(result.role)  # Output: Admin
        print(role2.role)  # Output: User

        # Representing objects as strings
        print(result)  # Output: Role(role_name='Admin')
        print(role2)  # Output: Role(role_name='User')
'''
        result = crud.checkUser(usn, psw)
        # ***********************************************

        logger.warning("-----> Result: {}".format(result))

        if result:

            if result.role == 'student':

                flash('You were successfully logged in as Student')
                # return render_template('admin_home.html')
                return redirect(url_for('student_home'))

            elif result.role == 'teacher':

                flash('You were successfully logged in as Teacher')
                # return render_template('super_admin_home.html')
                return redirect(url_for('teacher_home'))

        else:

            error = 'Invalid credentials'
            return render_template('login.html', error=error)

# -------------------------------------------------------------------------------------------------


@app.route('/student_signup', methods=['GET', 'POST'])
def student_signup():
    if request.method == 'GET':

        return render_template('student_signup.html')

    else:
        fname = str(request.form.get('fname'))
        lname = str(request.form.get('lname'))
        uname = str(request.form.get('uname'))
        email = str(request.form.get('email'))
        password = str(request.form.get('password'))
        role = str(request.form.get('role'))
        # course_id = request.form.getlist('course_id')

        logger.info("Fname: {} LName: {} UNamee: {} Email: {} password: {} role : {} ".format(
            fname, lname, uname, email, password, role))

        crud.createUser(fname, lname, uname, email, password, role)

        # return render_template('login.html')
        return redirect(url_for("student_signup_courses"))

# -------------------------------------------------------------------------------------------------


@app.route('/student_signup_courses', methods=['GET', 'POST'])
def student_signup_courses():
    if request.method == 'GET':

        result = crud.getallcourses()
        print("155 app.py type of result ----",type(result))
        print("156 app.py of result.userId ----*****=", result)

        logger.info("result{}".format(result))
        if result:
            data = result
        else:
            data = None

        return render_template('student_signup_courses.html', courseadd=result)
        #["apple", "banana", "cherry"])

    else:
        print("*************----168---***   post   method")
        course_Names = request.form.getlist('course_id')

        logger.info("course_id: {} ".format(course_Names))

        crud.insertcourse(course_Names)

        return render_template('login.html')

# -------------------------------------------------------------------------------------------------


@app.route('/teacher_signup', methods=['GET', 'POST'])
def teacher_signup():
    if request.method == 'GET':
        return render_template('teacher_signup.html')

    else:
        fname = str(request.form.get('fname'))
        lname = str(request.form.get('lname'))
        uname = str(request.form.get('uname'))
        email = str(request.form.get('email'))
        password = str(request.form.get('password'))
        role = str(request.form.get('role'))

        logger.info("Fname: {} LName: {} UNamee: {} Email: {} password: {} role : {}".format(
            fname, lname, uname, email, password, role))

        crud.createUser(fname, lname, uname, email, password, role)

        return render_template('login.html')

# -------------------------------------------------------------------------------------------------


@app.route('/teacher_home')
def teacher_home():

    return render_template('teacher_home.html')

# -------------------------------------------------------------------------------------------------


@app.route('/student_home')
def student_home():
    print (f"session.get(=====   line 214 :: {session.get('UID')}")
    return render_template('student_home.html')
    #return render_template('index.html')

# -------------------------------------------------------------------------------------------------


@app.route('/add', methods=['GET', 'POST'])
# @login_required
# @restricted(['teacher'])
def add():
    if request.method == 'GET':
        result = crud.getcourse()

        if result:
            data = result
        else:
            data = None

        return render_template('add.html', courses=data)
    else:
        course = str(request.form.get('course'))

    logger.info("course: {}".format(course))

    crud.addcourse(course)

    return redirect('/add')

# -------------------------------------------------------------------------------------------------


@app.route('/add_quiz', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'GET':

        result = crud.getcourse()

        if result:
            data = result
        else:
            data = None

        result1 = crud.get_Quiznames()

        if result1:
            data1 = result1
        else:
            data1 = None

        return render_template('add_quiz.html', courseadd=data, QuizNames=data1)

    else:

        course_id = request.form.get('course_id')
        quiz_name = str(request.form.get('quiz_name'))

        crud.add_quiz(quiz_name, course_id)

        logger.info("course_id: {} quiz name: {}".format(course_id, quiz_name))

        return redirect('/add_quiz')

# -------------------------------------------------------------------------------------------------


@app.route('/add_quiz_questions', methods=['GET', 'POST'])
def add_quiz_questions():
    if request.method == 'GET':

        result = crud.getcourse()

        if result:
            data = result
        else:
            data = None

        result1 = crud.get_Quiznames()

        if result1:
            data1 = result1
        else:
            data1 = None

        return render_template('add_quiz_questions.html', courseadd=data, QuizNames=data1)

    else:

        course_id = request.form.get('course_id')
        quiz_id = request.form.get('quiz_id')
        question = str(request.form.get('question'))
        option1 = str(request.form.get('option1'))
        option2 = str(request.form.get('option2'))
        option3 = str(request.form.get('option3'))
        option4 = str(request.form.get('option4'))
        correct_answer = [int(i)
                          for i in (request.form.getlist('correct_answer'))]

        final_options = [option1, option2, option3, option4]
        final_correct_answer = []

        logger.info(str(correct_answer))

        for i in range(1, len(final_options) + 1):
            if i in correct_answer:
                final_correct_answer.append(1)
            else:
                final_correct_answer.append(0)

        logger.info(str(final_correct_answer))

        crud.insertQuestionandAnswer(
            question, course_id,  final_options, final_correct_answer, quiz_id)

        logger.info("course_id: {} question: {} option1: {} option2: {} option3: {} option4 : {} correct_answer: {} quiz_id: {}".format(
            course_id, question, option1, option2, option3, option4, final_correct_answer, quiz_id))

        return render_template('add_quiz_questions.html')

# -------------------------------------------------------------------------------------------------


@app.route('/view_quiz', methods=['GET', 'POST'])
def view_quiz():

    if request.method == 'GET':
        # --------------- Course Dropdown--------
        result = crud.getcourse()
        logger.info("result{}".format(result))
        if result:
            data = result
        else:
            data = None
# --------------- Quiznames Dropdown----------
        result1 = crud.get_Quiznames()
        if result1:
            data3 = result1
        else:
            data3 = None

        return render_template('view_quiz.html', courseadd=data, QuizNames=data3, quizes='',  ans='')

    else:

        cid = request.form.get('course_id')
        qu_id = request.form.get('quiz_id')

        logger.info("course_id {} quiz_id {}".format(cid, qu_id))

        result = crud.getcourse()
        logger.info("result{}".format(result))
        if result:
            data = result
        else:
            data = None

        result1 = crud.get_Quiznames()

        if result1:
            data3 = result1
        else:
            data3 = None

        ques, answ = crud.getquizquestion(cid, qu_id)
        logger.info("query {}".format(ques))

        if ques:
            data1 = ques
        else:
            data1 = None

        if answ:
            data2 = answ
        else:
            data2 = None

        return render_template('view_quiz.html', courseadd=data, QuizNames=data3, ans=data2, quizes=data1)

# -------------------------------------------------------------------------------------------------


@app.route('/show_studentquiz', methods=['GET', 'POST'])
def show_studentquiz():

    if request.method == 'GET':

        # --------------- Course Dropdown--------
        result = crud.getcoursesdropdown()

        if result:
            data = result
        else:
            data = None

        logger.info("result:{}".format(result))
        print(f" data line 409====== {data}")
        return render_template('show_studentquiz.html', courseadd=data, quizes='',  ans='')

    else:

        
        c_id = request.form.get('course_id')
        qu_id = request.form.get('quiz_id')

        print(f" line 418  app  'course_id')={c_id}   quiz_id === {qu_id}  ")

        result = crud.getcoursesdropdown()

        if result:
            data = result
        else:
            data = None

        result1 = crud.get_QuiznamesStudent(c_id)

        if result1:
            data3 = result1
        else:
            data3 = None

        logger.info("result1{}".format(result1))

        ques, answ = crud.studentQuizQuestions(qu_id, c_id)
        logger.info("ques:{}, answ:{}".format(ques, answ))

        if ques and answ:
            data1, data2 = ques, answ
            session['C_ID'] = c_id
            session['QU_ID'] = qu_id
        else:
            data1, data2 = None, None

        return render_template('show_studentquiz.html', courseadd=data,  QuizNames=data3, quizes=data1, ans=data2)

# -------------------------------------------------------------------------------------------------


@app.route('/result_studentquiz', methods=['GET', 'POST'])
def result_studentquiz():

    if request.method == 'POST':
        selected_ans = []
        c_id = session.get('C_ID')

        qu_id = session.get('QU_ID')

        print(f"  line 458  c_id=course id =-- {c_id} qu_id= quiz id =  {qu_id}")
        logger.info("cid: {} quiz_id: {} ".format(c_id, qu_id))

        qauestion_count = crud.get_question_count(courseid=c_id, quizid=qu_id)
        logger.info("qauestion_count: {} ".format(qauestion_count))

        question_id = crud.get_question_id(courseid=c_id, quizid=qu_id)
        print(f"question_id  =={question_id}")







        logger.info("question_id: {} ".format(str(question_id)))

        selected_labels = {}
        for id in question_id:  # Replace quizes_ids with the list of question IDs
            selected_labels[id] = request.form.getlist('question_' + str(id))
        print("line 472  selected_labels =",selected_labels)
        print(f"len(question_id) = {len(question_id)}")

        #***************************

        question_id_int = [int(i) for i in question_id]
        print(f"  type of question_id { type(question_id)} ")
        new =[int(i) for i in question_id]

        print(f" len of new {len(new)}")
        print(f" new :__= {new}")

        # Fai qualcosa con questi ID come numeri interi
        # ...

        # Ora riportali a stringhe se necessario
        question_id_str = [str(i) for i in question_id_int]
        print(f"len(question_id_str) = {len(question_id_str)}")
        #**************

        for i in question_id_str:
            print(f"trying to sole {i}")

        selected_ansP = []
        for i in question_id:
            print(f" 485 selected_labels- {i} =={selected_labels[i]}")
            if '1' in selected_labels[i]:
                print("----line 487 ---------------========:::", i)
                selected_ansP.append(("True"))
            else:
                selected_ansP.append("False")
                print("----line 486 ---------------========:::", i)

        print("line 493 selected_ans=", selected_ansP)







        for i in question_id:
            print("  line 502 i =   ", i)
            print(f"selected_labels{i} =={selected_labels[i]}")
            a = request.form.getlist('question_' + str(i))
            gt=request.form.getlist('1')
            print("ggggt----506--------------hhhhhhhhhhhhhhhh:==",a)
            gtr = request.form.getlist('0')
            print("ggggtr------------------------508hhhhhhhhhhhhh:==",gtr)
            print("a:=================line509 app.py", str(a))

            if len(a) < 1:
                selected_ans.append(("False"))
            else:

                if '1' in selected_labels[i]:
                    print("----line 516---------------========:::",i)
                    print("----line 518 -------- selected_labels[i]---========:::", selected_labels[i])
                    selected_ans.append(("True"))

                else:
                    selected_ans.append("False")

        print("line 523selected_ans=",selected_ans)


        logger.info("Final set: {}".format(selected_ans))

        score = round((len([i for i in selected_ans if i == 'True']) / qauestion_count) * 100.0, 2)

        logger.info("Final Score: {}".format(score))
        print(f"result line 531   app {score}" )
        return render_template('results.html', score=score)


# -------------------------------------------------------------------------------------------------


@app.route('/my_courses', methods=['GET', 'POST'])
# @login_required
# @restricted(['teacher'])
def my_courses():
    if request.method == 'GET':

        # -----------Opted courses------
        print("***********************line 495************************")
        result = crud.getstudentcourse()
        if result:
            data = result
        else:
            data = None
# ---------To add more courses-------
        result1 = crud.getallcourses()
        logger.info("result{} result1{}".format(result, result1))
        if result1:
            data1 = result1
        else:
            data1 = None

        return render_template('my_courses.html', courses=data, courseadd=data1)

    else:
        course_Names = request.form.getlist('course_id')

        logger.info("course_id: {} ".format(course_Names))

        crud.insertcourseafterlogin(course_Names)

        return redirect(url_for("my_courses"))

# -------------------------------------------------------------------------------------------------


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == '__main__':
    app.run(debug=True)
