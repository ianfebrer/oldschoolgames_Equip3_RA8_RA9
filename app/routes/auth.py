from flask import render_template, Blueprint, request, jsonify, session, redirect
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login')
def login():
	return render_template('login.html')

@auth_bp.route('/register')
def register():
	return render_template('register.html')

@auth_bp.route('/logout')
def logout():
	session.pop('username', None)
	return redirect('/auth/login')
