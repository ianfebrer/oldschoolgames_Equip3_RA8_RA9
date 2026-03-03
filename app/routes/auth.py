from flask import render_template, Blueprint, request, jsonify
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
	if not username or not password:
		return jsonify({'success': False, 'message': 'Usuari o contranya requerits'})

	user = User(username, password)
	user.register()
	return jsonify({'success': True, 'message': 'Usuari registrat correctament'})
