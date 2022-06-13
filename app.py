from flask import Flask, request, render_template, redirect, url_for, flash
from werkzeug.utils import secure_filename
from admin import admin
from student import student
from lecturer import lecturer
import os
from os.path import join, dirname, realpath

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static\\uploads')

app = Flask(__name__)
app.secret_key = '5accdb11b2c10a78d7c92c5fa102ea77fcd50c2058b00f6e'
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH
app.register_blueprint(admin)
app.register_blueprint(student)
app.register_blueprint(lecturer)


@app.route('/')
def home():
    return render_template('home.html')


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True)
