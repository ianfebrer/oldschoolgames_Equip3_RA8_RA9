from flask import Blueprint, request, jsonify, session
from app.models.game_session import GameSession
from app.models.user import User

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Jocs reconeguts pel servidor (mateixos identificadors que envia el JavaScript)
JOCS_PERMESOS = ["pong", "trexpres", "memory"]


@api_bp.route('/sessions', methods=['POST'])
def api_sessions():
	data = request.get_json()
	if data is None:
		return jsonify({'success': False, 'message': 'No s\'ha rebut cap dada'}), 400

	username = session.get('username')
	if not username:
		return jsonify({'success': False, 'message': 'Cal iniciar sessió per guardar la puntuació'}), 401

	game_id = data.get('game_id')
	start_time = data.get('start_time')
	end_time = data.get('end_time')
	score = data.get('score')
	duration_ms = data.get('duration_ms')

	# score pot ser 0 (vàlid); comprovem explícitament None
	if not game_id or start_time is None or end_time is None or score is None or duration_ms is None:
		return jsonify({'success': False, 'message': 'Falten dades obligatòries (joc, temps, puntuació)'}), 400

	if game_id not in JOCS_PERMESOS:
		return jsonify({'success': False, 'message': 'Identificador de joc no permès'}), 400

	try:
		start_time = int(start_time)
		end_time = int(end_time)
		score = int(score)
		duration_ms = int(duration_ms)
	except (TypeError, ValueError):
		return jsonify({'success': False, 'message': 'Els valors numèrics no són vàlids'}), 400

	if score < 0 or duration_ms < 0 or start_time < 0 or end_time < 0:
		return jsonify({'success': False, 'message': 'Els valors no poden ser negatius'}), 400
	if end_time < start_time:
		return jsonify({'success': False, 'message': 'El temps de fi ha de ser posterior al d\'inici'}), 400

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
		return jsonify({'success': False, 'message': 'No s\'ha rebut cap dada'}), 400

	username = data.get('username')
	password = data.get('password')
	if not username or not password:
		return jsonify({'success': False, 'message': 'L\'usuari i la contrasenya són obligatoris'}), 400

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
		return jsonify({'success': False, 'message': 'No s\'ha rebut cap dada'}), 400

	username = data.get('username')
	password = data.get('password')
	if not username or not password:
		return jsonify({'success': False, 'message': 'L\'usuari i la contrasenya són obligatoris'}), 400

	try:
		user = User(username, password)
		success, message = user.login()
		if success:
			session['username'] = username
			return jsonify({'success': True, 'message': message, 'username': username})
		return jsonify({'success': False, 'message': message})
	except Exception as e:
		return jsonify({'success': False, 'message': str(e)}), 500
