from flask import Flask, redirect, render_template, url_for
from admin import admin

app = Flask(__name__)
app.register_blueprint(admin)


@app.route("/")
def home():
    return redirect('/admin/login')


if __name__ == '__main__':
    app.run(debug=True)
