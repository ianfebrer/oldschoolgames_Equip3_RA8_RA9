from flask import render_template, Blueprint, request, jsonify, session, redirect
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login')
def login():
	return render_template('login.html')

@auth_bp.route('/register')
def register():
	return render_template('register.html')

@auth_bp.route('/api/register', methods=['POST'])
def api_register():
	data = request.get_json()
	username = data.get('username')
	password = data.get('password')

	user = User(username, password)
	success, message = user.register()
	if success:
		return jsonify({'success': True, 'message': message})
	else:
		return jsonify({'success': False, 'message': message})

@auth_bp.route('/api/login', methods=['POST'])
def api_login():
	data = request.get_json()
	username = data.get('username')
	password = data.get('password')

	user = User(username, password)
	success, message = user.login()
	if success:
		session['username'] = username
		return jsonify({'success': True, 'message': message})
	else:
		return jsonify({'success': False, 'message': message})

@auth_bp.route('/logout')
def logout():
	session.pop('username', None)
	return redirect('/auth/login')
