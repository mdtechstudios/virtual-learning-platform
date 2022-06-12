from flask import Blueprint, render_template, redirect, url_for,flash, request, current_app, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TextAreaField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename
from database import db
import os

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
            return redirect(url_for('lecturer.home'))
    return render_template('lecturer/login.html',form=form)


# Lecturer Home Page
@lecturer.route('/', methods=['GET','POST'])
def home():
    email = "devadiga181@gmail.com"
    contents = db.contents.find({"lecturer":email})
    return render_template('lecturer/home.html',contents=contents)


@lecturer.route('/upload-content', methods=['GET','POST'])
def uploadcontent():
    email = "devadiga181@gmail.com"
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
            doc = {
                "file":filename,
                "ctype":ctype,
                "subject":subject,
                "lecturer":lecturer
            }
            res = db.contents.insert_one(doc)
            if res is not None:
                flash("Content Successfully Added!")
                return render_template('lecturer/upload-content.html',lecturer=lecturer,subjects=subjects)
            else:
                flash("Lecturer Not Added!")
                flash('Content Added successfully')
                return render_template('lecturer/upload-content.html',lecturer=lecturer,subjects=subjects)
            
        return render_template('lecturer/upload-content.html',lecturer=lecturer,subjects=subjects)
    return render_template('lecturer/upload-content.html',lecturer=lecturer,subjects=subjects)


# Lecturer Login Form
class LecturerLogin(FlaskForm):
    email = EmailField('Enter your email', validators=[DataRequired('Please enter your email')])
    password = PasswordField('Enter your password',validators=[DataRequired('Please enter your password')])
