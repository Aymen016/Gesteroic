from flask import Blueprint, request, jsonify
from user.models import User

# Define a Blueprint for user-related routes
user_bp = Blueprint('user', __name__)

@user_bp.route('/signup', methods=['POST'])
def signup():
    return User().signup()

@user_bp.route('/signout')
def signout():
    return User().signout()

@user_bp.route('/login', methods=['POST'])
def login():
    return User().login()