from flask import Blueprint, render_template
from database import mongo

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/login')
def login():
    online_users = mongo.db.users.find({"online": True})
    return render_template('admin/login.html',online_users=online_users)

@admin.route('/')
def home():
    return "Home"