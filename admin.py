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


# View All semesters
@admin.route('/semesters', methods=['GET','POST'])
def viewsemesters():
    semesters = db.semesters.find()
    return render_template('admin/view-semesters.html',semesters=semesters)


# View All subjects
@admin.route('/subjects', methods=['GET','POST'])
def viewsubjects():
    subjects = db.subjects.find()
    return render_template('admin/view-subjects.html',subjects=subjects)



# View All Students
@admin.route('/students', methods=['GET','POST'])
def viewstudents():
    students = db.students.find()
    return render_template('admin/view-students.html',students=students)


# Delete Student
@admin.route('/delete-student/<email>')
def deletestudent(email):
    qry = {
        "email": email
    }
    res =  db.students.delete_one(qry)
    print(res)
    flash("Student removed")
    return redirect(url_for('admin.viewstudents'))



# Delete Subjects
@admin.route('/delete-subjects/<code>')
def deletesub(code):
    qry = {
        "code": code
    }
    res =  db.subjects.delete_one(qry)
    print(res)
    flash("Subject removed")
    return redirect(url_for('admin.viewsubjects'))



# Delete Semesters
@admin.route('/delete-semester/<code>')
def deletesem(code):
    qry = {
        "code": code
    }
    res =  db.semesters.delete_one(qry)
    print(res)
    flash("Semester removed")
    return redirect(url_for('admin.viewsemesters'))


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
            flash("Lecturer Not Added!")
            return render_template('admin/add-lecturer.html',semesters=semesters,subjects=subjects)
    return render_template('admin/add-lecturer.html',semesters=semesters,subjects=subjects)


# Delete Lecturer
@admin.route('/delete-lecturer/<email>')
def deletelecturer(email):
    qry = {
        "email": email
    }
    res =  db.lecturers.delete_one(qry)
    print(res)
    flash("Lecturer removed")
    return redirect(url_for('admin.viewlecturers'))


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


# Add semester
@admin.route('/add-semester',methods=['GET','POST'])
def addsem():
    subjects = db.subjects.find()
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        subjects = request.form.getlist('subjects[]')
        doc = {
            "name":name,
            "code":code,
            "subjects":subjects
        }
        res = db.semesters.insert_one(doc)
        if res is not None:
            flash("Semester Successfully Added!")
            return render_template('admin/add-sem.html',subjects=subjects)
        else:
            flash("Semester Not Added!")
            return render_template('admin/add-sem.html',subjects=subjects)
        return render_template('admin/add-sem.html',subjects=subjects)
    return render_template('admin/add-sem.html',subjects=subjects)



# Add semester
@admin.route('/add-subject',methods=['GET','POST'])
def addsub():
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        info = request.form.get('info')
        doc = {
            "name":name,
            "code":code,
            "info":info
        }
        res = db.subjects.insert_one(doc)
        if res is not None:
            flash("Subject Successfully Added!")
            return render_template('admin/add-sub.html')
        else:
            flash("Subject Not Added!")
            return render_template('admin/add-sub.html')
        return render_template('admin/add-sub.html')
    return render_template('admin/add-sub.html')


# Admin Login Form
class AdminLogin(FlaskForm):
    email = EmailField('Enter your email', validators=[DataRequired('Please enter your email')])
    password = PasswordField('Enter your password',validators=[DataRequired('Please enter your password')])
