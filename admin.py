from flask import Blueprint, render_template, redirect, url_for,flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TextAreaField
from wtforms.validators import DataRequired
from database import db

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Admin Dashboard
@admin.route('/', methods=['GET','POST'])
def home():
    return render_template('admin/home.html')


# View All Lecturers
@admin.route('/lecturers', methods=['GET','POST'])
def viewlecturers():
    data = db.lecturers.find()
    return render_template('admin/view-lecturers.html',lecturers=data)


# Add Lecturer
@admin.route('/add-lecturers', methods=['GET','POST'])
def addlecturers():
    semdata = db.semesters.find()
    subdata = db.subjects.find()
    if request.method == 'POST':
        data = request.form
        print(data)
        return data
    return render_template('admin/add-lecturer.html',semesters=semdata,subjects=subdata)


# Admin Login
@admin.route('/login', methods=['GET','POST'])
def login():
    form = AdminLogin()
    if form.validate_on_submit():
        email = form.data.get('email')
        password = form.data.get('password')
        data = {
            "email":email,
            "password":password
        }
        res = db.admin.find_one(data)
        if res is None:
            flash("Invalid Email/Password")
            render_template('admin/login.html',form=form)
        else:
            return redirect(url_for('admin.home'))
    return render_template('admin/login.html',form=form)


# Admin Login Form
class AdminLogin(FlaskForm):
    email = EmailField('Enter your email', validators=[DataRequired('Please enter your email')])
    password = PasswordField('Enter your password',validators=[DataRequired('Please enter your password')])
