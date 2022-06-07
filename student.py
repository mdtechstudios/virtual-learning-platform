from flask import Blueprint, render_template, redirect, url_for,flash, request,jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TextAreaField, IntegerField
from wtforms.validators import DataRequired
from database import db

student = Blueprint('student', __name__, url_prefix='/student')

# Student Dashboard
@student.route('/', methods=['GET','POST'])
def home():
    return render_template('student/home.html')

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
            return redirect(url_for('student.home'))
    return render_template('student/login.html',form=form)


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
