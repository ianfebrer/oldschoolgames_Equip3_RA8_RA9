from flask import Blueprint, request, jsonify, session
from app.models.game_session import GameSession
from app.models.user import User
from app.models.game_event import GameEvent
from app.models.game_state import GameState
from app.models.game_log import GameLog
import uuid
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Jocs reconeguts pel servidor (mateixos identificadors que envia el JavaScript)
JOCS_PERMESOS = ["pong", "trexpres", "memory"]


@api_bp.route('/sessions', methods=['POST'])
def api_sessions():
	data = request.get_json()
	if data is None:
		return jsonify({'success': False, 'message': 'No data received'}), 400

	username = session.get('username')
	if not username:
		return jsonify({'success': False, 'message': 'Authentication required to save scores'}), 401

	game_id = data.get('game_id')
	start_time = data.get('start_time')
	end_time = data.get('end_time')
	score = data.get('score')
	duration_ms = data.get('duration_ms')

	# score pot ser 0 (vàlid); comprovem explícitament None
	if not game_id or start_time is None or end_time is None or score is None or duration_ms is None:
		return jsonify({'success': False, 'message': 'Missing required fields (game, time, score)'}), 400

	if game_id not in JOCS_PERMESOS:
		return jsonify({'success': False, 'message': 'Invalid game identifier'}), 400

	try:
		start_time = int(start_time)
		end_time = int(end_time)
		score = int(score)
		duration_ms = int(duration_ms)
	except (TypeError, ValueError):
		return jsonify({'success': False, 'message': 'Invalid numeric values'}), 400

	if score < 0 or duration_ms < 0 or start_time < 0 or end_time < 0:
		return jsonify({'success': False, 'message': 'Values cannot be negative'}), 400
	if end_time < start_time:
		return jsonify({'success': False, 'message': 'End time must be after start time'}), 400

	try:
		game_session = GameSession(game_id, username, start_time, end_time, score, duration_ms)
		success, message = game_session.save()
		if success:
			return jsonify({'success': True, 'message': message})
		return jsonify({'success': False, 'message': message}), 400
	except Exception as e:
		return jsonify({'success': False, 'message': str(e)}), 500


@api_bp.route('/register', methods=['POST'])
def api_register():
	data = request.get_json()
	if data is None:
		return jsonify({'success': False, 'message': 'No data received'}), 400

	username = data.get('username')
	password = data.get('password')
	if not username or not password:
		return jsonify({'success': False, 'message': 'Username and password are required'}), 400

	try:
		user = User(username, password)
		success, message = user.register()
		if success:
			return jsonify({'success': True, 'message': message})
		return jsonify({'success': False, 'message': message})
	except Exception as e:
		return jsonify({'success': False, 'message': str(e)}), 500


@api_bp.route('/login', methods=['POST'])
def api_login():
	data = request.get_json()
	if data is None:
		return jsonify({'success': False, 'message': 'No data received'}), 400

	username = data.get('username')
	password = data.get('password')
	if not username or not password:
		return jsonify({'success': False, 'message': 'Username and password are required'}), 400

	try:
		user = User(username, password)
		success, message = user.login()
		if success:
			session['username'] = username
			return jsonify({'success': True, 'message': message, 'username': username})
		return jsonify({'success': False, 'message': message})
	except Exception as e:
		return jsonify({'success': False, 'message': str(e)}), 500


@api_bp.route('/events', methods=['POST'])
def api_events():
	data = request.get_json()
	if not data:
		return jsonify({'success': False, 'message': 'No dades'}), 400

	game_id = data.get('game_id')
	username = session.get('username', 'guest')
	event_type = data.get('event_type')
	event_data = data.get('data', {})

	try:
		event = GameEvent(game_id, username, event_type, event_data)
		event_id = event.save_to_mongo()
		return jsonify({'success': True, 'event_id': str(event_id)})
	except Exception as e:
		return jsonify({'success': False, 'message': str(e)}), 500


@api_bp.route('/states', methods=['POST'])
def api_states():
	data = request.get_json()
	if not data:
		return jsonify({'success': False, 'message': 'No dades'}), 400

	game_id = data.get('game_id')
	username = session.get('username', 'guest')
	state_data = data.get('state_data', {})

	try:
		state = GameState(game_id, username, state_data)
		state_id = state.save_to_mongo()
		return jsonify({'success': True, 'state_id': str(state_id)})
	except Exception as e:
		return jsonify({'success': False, 'message': str(e)}), 500


@api_bp.route('/logs/start', methods=['POST'])
def api_logs_start():
	data = request.get_json() or {}
	game_id = data.get('game_id')
	username = session.get('username', 'guest')
	session_id = data.get('session_id') or str(uuid.uuid4())

	try:
		log = GameLog(game_id, username, session_id)
		log.save_to_mongo()
		return jsonify({'success': True, 'session_id': session_id})
	except Exception as e:
		return jsonify({'success': False, 'message': str(e)}), 500


@api_bp.route('/logs/end', methods=['POST'])
def api_logs_end():
	data = request.get_json()
	if not data:
		return jsonify({'success': False, 'message': 'No dades'}), 400

	game_id = data.get('game_id')
	username = session.get('username', 'guest')
	session_id = data.get('session_id')
	final_score = data.get('final_score')

	if not session_id:
		return jsonify({'success': False, 'message': 'session_id obligatori'}), 400

	try:
		log = GameLog(game_id, username, session_id)
		log.close_log(final_score)
		log.save_to_mongo()
		return jsonify({'success': True, 'session_id': session_id})
	except Exception as e:
		return jsonify({'success': False, 'message': str(e)}), 500
