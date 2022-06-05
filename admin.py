from flask import Blueprint, render_template, redirect, url_for,flash, request,jsonify
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
    lecturers = db.lecturers.find()
    return render_template('admin/view-lecturers.html',lecturers=lecturers)



# View All Students
@admin.route('/students', methods=['GET','POST'])
def viewstudents():
    students = db.students.find()
    return render_template('admin/view-students.html',students=students)


# Add Lecturer
@admin.route('/add-lecturers', methods=['GET','POST'])
def addlecturers():
    semesters = db.semesters.find()
    subjects = db.subjects.find()
    if request.method == 'POST':
        # data = request.form
        fname = request.form.get('fname')
        subs = request.form.getlist('subjects[]')
        sems = request.form.getlist('semesters[]')
        email = request.form.get('email')
        password = request.form.get('password')
        info = request.form.get('info')
        doc = {
            "name": fname,
            "email": email,
            "password": password,
            "semesters": sems,
            "subjects":subs,
            "info": info
        }
        res = db.lecturers.insert_one(doc)
        if res is not None:
            flash("Lecturer Successfully Added!")
            return render_template('admin/add-lecturer.html',semesters=semesters,subjects=subjects)
        else:
            flash("SomeLecturer Not Added!")
            return render_template('admin/add-lecturer.html',semesters=semesters,subjects=subjects)
    return render_template('admin/add-lecturer.html',semesters=semesters,subjects=subjects)


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
