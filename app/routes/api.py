from flask import Blueprint, request, jsonify, session
from app.models.game_session import GameSession
from app.models.game_event import GameEvent
from app.models.game_state import GameState
from app.models.game_log import GameLog
import uuid
from app.models.user import User
api_bp = Blueprint('api', __name__, url_prefix='/api')

# =========================================================
# RUTA IAN: GUARDAR PUNTUACIONS (SESSIONS A MARIADB)
# =========================================================
@api_bp.route('/sessions', methods=['POST'])
def api_sessions():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No s’han rebut dades'}), 400

    # Obtenim l'usuari de la sessió de Flask (gestionada per l'Adrià)
    username = session.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'Cal estar autenticat per guardar puntuacions'}), 401

    # Dades enviades pel joc (JS)
    game_id = data.get('game_id') 
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    score = data.get('score')
    duration_ms = data.get('duration_ms', 0)

    if not game_id or score is None:
        return jsonify({'success': False, 'message': 'Falten camps obligatòries'}), 400

    try:
        # Instanciem el model de la teva part
        new_session = GameSession(
            game_id=game_id,
            username=username,
            start_time=start_time,
            end_time=end_time,
            score=score,
            duration_ms=duration_ms
        )
        
        # El mètode save() ha de gestionar la inserció a MariaDB (taula scores)
        success, message = new_session.save()
        
        if success:
            return jsonify({'success': True, 'message': message}), 201
        else:
            return jsonify({'success': False, 'message': message}), 500

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# =========================================================
# RUTES GABRIEL: LOGS I ESTATS (MONGODB)
# =========================================================
@api_bp.route('/state', methods=['POST'])
def api_state():
    data = request.get_json() or {}
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
    data = request.get_json() or {}
    session_id = data.get('session_id')
    if not session_id:
        return jsonify({'success': False, 'message': 'session_id obligatori'}), 400

    try:
        # Aquí Gabriel tancaria el log a Mongo
        return jsonify({'success': True, 'message': 'Log finalitzat'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
    
