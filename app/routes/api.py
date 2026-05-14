from flask import Blueprint, request, jsonify, session
from app.models.game_session import GameSession
from app.models.user import User
from app.models.game_result import GameResult

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Jocs reconeguts pel servidor (mateixos identificadors que envia el JavaScript)
JOCS_PERMESOS = ["pong", "trexpres", "memory"]

@api_bp.route('/sessions', methods=['POST'])
def api_sessions():
    data = request.get_json()
    if data is None:
        return jsonify({'success': False, 'message': 'No s\'ha rebut cap dada'}), 400

    # 1. Validació d'usuari (indispensable per saber de qui és la puntuació)
    username = session.get('username')
    user_id = session.get('user_id') # Assegura't que el login desa l'ID a la sessió
    
    if not username:
        return jsonify({'success': False, 'message': 'Cal iniciar sessió per guardar la puntuació'}), 401

    # 2. Recollida de dades
    game_id = data.get('game_id')
    score = data.get('score')
    duration_ms = data.get('duration_ms')
    # Recollim dades extres per a MongoDB (si el JS les envia, si no, diccionari buit)
    details = data.get('details', {}) 

    # 3. Validacions bàsiques
    if not game_id or score is None or duration_ms is None:
        return jsonify({'success': False, 'message': 'Falten dades obligatòries'}), 400

    if game_id not in JOCS_PERMESOS:
        return jsonify({'success': False, 'message': 'Joc no reconegut'}), 400

    try:
        # Intentem convertir a enters per seguretat
        score = int(score)
        duration_ms = int(duration_ms)
        
        # 4. ÚS DE LA TEVA CLASSE (POO)
        # Instanciem l'objecte amb la lògica de guardat dual
        from app.models.game_result import GameResult
        resultat = GameResult(
            user_id=user_id, 
            game_slug=game_id, 
            score=score, 
            duration_ms=duration_ms, 
            details=details
        )
        
        # Cridem al mètode save() que tu has creat
        if resultat.save():
            return jsonify({
                'success': True, 
                'message': f'Partida de {username} guardada a MariaDB (Top 10) i MongoDB (Logs)'
            })
        else:
            return jsonify({'success': False, 'message': 'Error en l\'escriptura a les bases de dades'}), 500

    except ValueError:
        return jsonify({'success': False, 'message': 'Dades numèriques no vàlides'}), 400
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
