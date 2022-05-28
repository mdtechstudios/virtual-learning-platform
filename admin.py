from flask import Blueprint, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TextAreaField
from wtforms.validators import DataRequired
from database import client

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Admin Login Route
@admin.route('/login',methods=['GET','POST'])
def login():
    form = AdminLogin()
    if form.validate_on_submit():
        email = form.data.get('email')
        password = form.data.get('password')
        res = client.db.admin.find_one({"email":email,"password":password})
        if res is None:
            msg = "Invalid Email/Password"
            render_template('admin/login.html',form=form, msg=msg)
        else:
            return redirect(url_for('admin.dashboard'))
    return render_template('admin/login.html',form=form)

# Admin Login Form
class AdminLogin(FlaskForm):
    email = EmailField('Enter your email', validators=[DataRequired('Please enter email')])
    password = PasswordField('Enter your password',validators=[DataRequired('Please enter password')])


# Admin Dashboard Route
@admin.route('/dashboard',methods=['GET','POST'])
def dashboard():
    return render_template('admin/dashboard.html')


# Add Lecturer
@admin.route('/add-lecturer',methods=['GET','POST'])
def addlecturer():
    form = AddLecturer()
    if form.validate_on_submit():
        name= form.data.get('name')
        email=form.data.get('email')
        password=form.data.get('password')
        info=form.data.get('info')
        doc = {"name":name,"email":email,"password":password,"info":info}
        res = client.db.lecturers.insert_one(doc)
        if res is not None:
            msg="Lecturer Added"
            return render_template('admin/add-lecturer.html',form=form,msg=msg)
        else:
            msg="Lecturer Not Added"
            return render_template('admin/add-lecturer.html',form=form,msg=msg)
    return render_template('admin/add-lecturer.html',form=form)


# Admin Lecturer Form
class AddLecturer(FlaskForm):
    name = StringField('Enter Full Name',validators=[DataRequired()])
    email = EmailField('Enter email', validators=[DataRequired('Please enter email')])
    password = PasswordField('Enter password',validators=[DataRequired('Please enter password')])
    info = TextAreaField('Enter Information',validators=[DataRequired()])


# View Lecturer
@admin.route('/view-lecturer',methods=['GET','POST'])
def viewlecturer():
    data=client.db.lecturers.find()
    return render_template('admin/view-lecturer.html',lecturers=data)



@admin.route('/')
def home():
    return "Home"