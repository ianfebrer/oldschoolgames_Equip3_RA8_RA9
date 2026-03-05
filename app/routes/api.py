from flask import Blueprint, request, jsonify, session
from app.models.game_session import GameSession
from app.models.user import User

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/sessions', methods=['POST'])
def api_sessions():
	data = request.get_json()
	username = data.get('username')
	game_id = data.get('game_id')
	start_time = data.get('start_time')
	end_time = data.get('end_time')
	score = data.get('score')

	game_session = GameSession(game_id, username, start_time, end_time, score)
	success, message = game_session.create()
	if success:
		return jsonify({'success': True, 'message': message})
	else:
		return jsonify({'success': False, 'message': message})


@api_bp.route('/register', methods=['POST'])
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

@api_bp.route('/login', methods=['POST'])
def api_login():
	data = request.get_json()
	username = data.get('username')
	password = data.get('password')

	user = User(username, password)
	success, message = user.login()
	if success:
		session['username'] = username
		return jsonify({'success': True, 'message': message, 'username': username})
	else:
		return jsonify({'success': False, 'message': message})
