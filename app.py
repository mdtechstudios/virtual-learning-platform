from flask import Flask
from admin import admin
from student import student

app = Flask(__name__)
app.secret_key = '5accdb11b2c10a78d7c92c5fa102ea77fcd50c2058b00f6e'
app.register_blueprint(admin)
app.register_blueprint(student)


if __name__ == '__main__':
    app.run(debug=True)
