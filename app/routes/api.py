from flask import Blueprint, request, jsonify, session
import uuid

# Importacions dels models de tots els membres de l'equip
from app.models.user import User                   # Adrià
from app.models.game_result import GameResult      # Ian
from app.models.game_event import GameEvent        # Gabriel
from app.models.game_state import GameState        # Gabriel
from app.models.game_log import GameLog            # Gabriel

api_bp = Blueprint('api', __name__, url_prefix='/api')

JOCS_PERMESOS = ["pong", "trexpres", "memory"]

# =====================================================================
# RUTES ADRIÀ (SISTEMA D'USUARIS)
# =====================================================================
@api_bp.route('/register', methods=['POST'])
def api_register():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No s\'han rebut dades'}), 400

    username = data.get('username')
    password = data.get('password')
    
    try:
        user = User(username, password)
        success, message = user.register()
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/login', methods=['POST'])
def api_login():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'No s\'han rebut dades'}), 400

    username = data.get('username')
    password = data.get('password')

    try:
        user = User(username, password)
        success, message = user.login()
        if success:
            session['username'] = username
            return jsonify({'success': True, 'message': message, 'username': username})
        return jsonify({'success': False, 'message': message})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# =====================================================================
# RUTA IAN (GUARDAT DE PARTIDES - MARIADB i MONGODB)
# =====================================================================
@api_bp.route('/sessions', methods=['POST'])
def api_sessions():
    data = request.get_json()
    if data is None:
        return jsonify({'success': False, 'message': 'No s\'ha rebut cap dada'}), 400

    username = session.get('username')
    if not username:
        return jsonify({'success': False, 'message': 'Cal iniciar sessió per guardar la puntuació'}), 401

    game_id = data.get('game_id')
    score = data.get('score')
    duration_ms = data.get('duration_ms')
    details = data.get('details', {}) 

    if not game_id or score is None or duration_ms is None:
        return jsonify({'success': False, 'message': 'Falten dades obligatòries'}), 400

    if game_id not in JOCS_PERMESOS:
        return jsonify({'success': False, 'message': 'Joc no reconegut'}), 400

    try:
        score = int(score)
        duration_ms = int(duration_ms)
        
        # SOLUCIÓ IAN: Obtenim l'ID aquí perquè l'Adrià no l'ha posat a la sessió
        from app.database import get_connection
        user_id = None
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
                user_db = cursor.fetchone()
                if user_db:
                    user_id = user_db['id']
                    
        if not user_id:
            return jsonify({'success': False, 'message': 'Error: Usuari no trobat a la base de dades (Top 10)'}), 404

        # Ús de la teva classe GameResult
        resultat = GameResult(
            user_id=user_id, 
            game_slug=game_id, 
            score=score, 
            duration_ms=duration_ms, 
            details=details
        )
        
        if resultat.save():
            return jsonify({'success': True, 'message': f'Partida de {username} guardada a MariaDB i MongoDB'})
        else:
            return jsonify({'success': False, 'message': 'Error en l\'escriptura a les bases de dades'}), 500

    except ValueError:
        return jsonify({'success': False, 'message': 'Dades numèriques no vàlides'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500


# =====================================================================
# RUTES GABRIEL (DADES EN TEMPS REAL - MONGODB)
# =====================================================================
@api_bp.route('/events', methods=['POST'])
def api_events():
    data = request.get_json() or {}
    try:
        event = GameEvent(data.get('game_id'), session.get('username', 'guest'), data.get('event_type'), data.get('data', {}))
        event_id = event.save_to_mongo()
        return jsonify({'success': True, 'event_id': str(event_id)})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/states', methods=['POST'])
def api_states():
    data = request.get_json() or {}
    try:
        state = GameState(data.get('game_id'), session.get('username', 'guest'), data.get('state_data', {}))
        state_id = state.save_to_mongo()
        return jsonify({'success': True, 'state_id': str(state_id)})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@api_bp.route('/logs/start', methods=['POST'])
def api_logs_start():
    data = request.get_json() or {}
    session_id = data.get('session_id') or str(uuid.uuid4())
    try:
        log = GameLog(data.get('game_id'), session.get('username', 'guest'), session_id)
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
        log = GameLog(data.get('game_id'), session.get('username', 'guest'), session_id)
        log.close_log(data.get('final_score'))
        log.save_to_mongo()
        return jsonify({'success': True, 'session_id': session_id})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
