from flask import Blueprint, render_template, redirect, url_for,flash, request, current_app, jsonify, session
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TextAreaField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from database import db
import os
import uuid

lecturer = Blueprint('lecturer', __name__, url_prefix='/lecturer')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4','mp3'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Lecturer Login
@lecturer.route('/login', methods=['GET','POST'])
def login():
    form = LecturerLogin()
    if form.validate_on_submit():
        email = form.data.get('email')
        password = form.data.get('password')
        data = {
            "email":email,
            "password":password
        }
        res = db.lecturers.find_one(data)
        print(res)
        if res is None:
            flash("Invalid Email/Password")
            render_template('lecturer/login.html',form=form)
        else:
            session["l_email"] = email
            return redirect(url_for('lecturer.home'))
    return render_template('lecturer/login.html',form=form)



@lecturer.route('/logout')
def logout():
    session['l_email'] = None
    return redirect(url_for('lecturer.login'))

def isLoggedIn():
    if session.get('l_email') == None:
        print(session.get('l_email') == None)
        return False
    else:
        #return redirect(url_for(request.url))
        return True



# Lecturer Home Page
@lecturer.route('/', methods=['GET','POST'])
def home():
    if not isLoggedIn():
        return redirect(url_for('lecturer.login'))
    email = session.get("l_email")
    contents = db.contents.find({"lecturer":email})
    return render_template('lecturer/home.html',contents=contents)


@lecturer.route('/upload-content', methods=['GET','POST'])
def uploadcontent():
    email = session.get("l_email")
    lecturer = db.lecturers.find_one({"email":email})
    subjects = db.subjects.find()
    if request.method == 'POST':
        ctype = request.form.get('ctype')
        subject = request.form.get('subject')
        lecturer = request.form.get('lecturer')
        if 'file' not in request.files:
            flash('No file part')
            return render_template('lecturer/upload-content.html',lecturer=lecturer,subjects=subjects)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return render_template('lecturer/upload-content.html',lecturer=lecturer,subjects=subjects)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            uid = uuid.uuid4().hex
            doc = {
                "file":filename,
                "ctype":ctype,
                "subject":subject,
                "lecturer":lecturer,
                "uid":uid
            }
            res = db.contents.insert_one(doc)
            if res is not None:
                flash("Content Successfully Added!")
                return render_template('lecturer/upload-content.html',lecturer=lecturer,subjects=subjects)
            else:
                flash("Lecturer Not Added!")
                flash('Content Added successfully')
                return redirect(url_for('lecturer.home'))
            
        return render_template('lecturer/upload-content.html',lecturer=lecturer,subjects=subjects)
    return render_template('lecturer/upload-content.html',lecturer=lecturer,subjects=subjects)


@lecturer.route('/delete-content/<id>', methods=['GET','POST'])
def deletecontent(id):
    res =  db.contents.delete_one({"uid":id})
    print(res)
    if res is None:
        flash('Content Not Deleted')
    else:
        flash('Content Removed')
    return redirect(url_for('lecturer.home'))

# Lecturer Login Form
class LecturerLogin(FlaskForm):
    email = EmailField('Enter your email', validators=[DataRequired('Please enter your email')])
    password = PasswordField('Enter your password',validators=[DataRequired('Please enter your password')])
