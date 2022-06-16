from flask import Blueprint, render_template, redirect, url_for,flash, request,jsonify, session
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import DataRequired
from database import db

student = Blueprint('student', __name__, url_prefix='/student')

# Student Dashboard
@student.route('/', methods=['GET','POST'])
def home():
    if not isLoggedIn():
        return redirect(url_for('student.login'))
    semesters = db.semesters.find()
    subjects = db.subjects.find()
    contents = db.contents.find()
    return render_template('student/home.html',semesters=semesters,subjects=subjects,contents=contents)


@student.route('/subjects/<semcode>')
def subjects(semcode):
    semesters = db.semesters.find()
    all_subjects = db.subjects.find()
    contents = db.contents.find()
    sub = db.semesters.find_one({"code":semcode})
    print(sub)
    return render_template('student/subjects.html',semesters=semesters,subjects=sub,all_subjects=all_subjects,contents=contents)


@student.route('/contents/<subcode>')
def contents(subcode):
    semesters = db.semesters.find()
    all_subjects = db.subjects.find_one({"code":subcode})
    contents = db.contents.find({"subject":subcode})
    return render_template('student/contents.html',semesters=semesters,all_subjects=all_subjects,contents=contents)

@student.route('/lecturer-info/<lectemail>')
def lecturerinfo(lectemail):
    lecturer = db.lecturers.find_one({"email":lectemail})
    return render_template('student/lecturer-info.html',lecturer=lecturer)


# Student Register
@student.route('/register', methods=['GET','POST'])
def register():
    form = StudentRegister()
    if form.validate_on_submit():
        doc = form.data
        # name = form.data.get('name')
        # email = form.data.get('email')
        # phoneno = form.data.get('phoneno')
        # password = form.data.get('password')
        # doc = {
        #     name: name,
        #     email: email,
        #     phoneno: phoneno,
        #     password: password
        # }
        print(doc)
        res = db.students.insert_one(doc)
        print(res)
        if res is not None:
            flash("Account Successfully Created!")
            return redirect(url_for('student.login'))
        else:
            flash("Account not created")
            return render_template('student/register.html',form=form)
    return render_template('student/register.html',form=form)


# Student Login
@student.route('/login', methods=['GET','POST'])
def login():
    form = StudentLogin()
    if form.validate_on_submit():
        email = form.data.get('email')
        password = form.data.get('password')
        data = {
            "email":email,
            "password":password
        }
        res = db.students.find_one(data)
        print(res)
        if res is None:
            flash("Invalid Email/Password")
            render_template('student/login.html',form=form)
        else:
            session["student_email"] = email
            return redirect(url_for('student.home'))
    return render_template('student/login.html',form=form)


@student.route('/logout')
def logout():
    session['student_email'] = None
    return redirect(url_for('student.login'))

def isLoggedIn():
    if session.get('student_email') == None:
        print(session.get('student_email') == None)
        return False
    else:
        #return redirect(url_for(request.url))
        return True


# Student Login Form
class StudentLogin(FlaskForm):
    email = EmailField('Enter your email', validators=[DataRequired('Please enter your email')])
    password = PasswordField('Enter your password',validators=[DataRequired('Please enter your password')])


# Student Register Form
class StudentRegister(FlaskForm):
    name = StringField('Enter your name',validators=[DataRequired('Please enter your name')])
    phoneno = StringField('Enter phone number',validators=[DataRequired('Please enter valid phone number')])
    email = EmailField('Enter your email', validators=[DataRequired('Please enter your email')])
    password = PasswordField('Enter your password',validators=[DataRequired('Please enter your password')])
