from flask import Blueprint, request, jsonify, session

from app.models.game_session import GameSession
from app.models.user import User
from app.models.game_event import GameEvent
from app.models.game_state import GameState
from app.models.game_log import GameLog
from app.models.game_result import GameResult

from app.translations import t

import uuid

api_bp = Blueprint('api', __name__, url_prefix='/api')

JOCS_PERMESOS = ["pong", "trexpres", "memory"]

# =====================================================================
# RUTES ADRIÀ (SISTEMA D'USUARIS)
# =====================================================================

@api_bp.route('/register', methods=['POST'])
def api_register():

    data = request.get_json()
    lang = session.get('lang', 'en')

    if data is None:
        return jsonify({
            'success': False,
            'message': t('no_data_received', lang)
        }), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({
            'success': False,
            'message': t('username_password_required', lang)
        }), 400

    try:
        user = User(username, password)
        success, message = user.register()

        return jsonify({
            'success': success,
            'message': t(message, lang)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@api_bp.route('/login', methods=['POST'])
def api_login():

    data = request.get_json()
    lang = session.get('lang', 'en')

    if data is None:
        return jsonify({
            'success': False,
            'message': t('no_data_received', lang)
        }), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({
            'success': False,
            'message': t('username_password_required', lang)
        }), 400

    try:
        user = User(username, password)
        success, message = user.login()

        if success:
            session['username'] = username

            return jsonify({
                'success': True,
                'message': t(message, lang),
                'username': username
            })

        return jsonify({
            'success': False,
            'message': t(message, lang)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# =====================================================================
# RUTA IAN + MASTER (GUARDAT DE PARTIDES)
# =====================================================================

@api_bp.route('/sessions', methods=['POST'])
def api_sessions():

    data = request.get_json()
    lang = session.get('lang', 'en')

    if data is None:
        return jsonify({
            'success': False,
            'message': t('no_data_received', lang)
        }), 400

    username = session.get('username')

    if not username:
        return jsonify({
            'success': False,
            'message': t('auth_required_scores', lang)
        }), 401

    game_id = data.get('game_id')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    score = data.get('score')
    duration_ms = data.get('duration_ms')
    details = data.get('details', {})

    if (
        not game_id or
        start_time is None or
        end_time is None or
        score is None or
        duration_ms is None
    ):
        return jsonify({
            'success': False,
            'message': t('missing_required_fields', lang)
        }), 400

    if game_id not in JOCS_PERMESOS:
        return jsonify({
            'success': False,
            'message': t('invalid_game_id', lang)
        }), 400

    try:
        start_time = int(start_time)
        end_time = int(end_time)
        score = int(score)
        duration_ms = int(duration_ms)

    except (TypeError, ValueError):
        return jsonify({
            'success': False,
            'message': t('invalid_numeric_values', lang)
        }), 400

    if score < 0 or duration_ms < 0 or start_time < 0 or end_time < 0:
        return jsonify({
            'success': False,
            'message': t('negative_values_error', lang)
        }), 400

    if end_time < start_time:
        return jsonify({
            'success': False,
            'message': t('end_time_error', lang)
        }), 400

    try:

        # =========================
        # MASTER -> GameSession
        # =========================

        game_session = GameSession(
            game_id,
            username,
            start_time,
            end_time,
            score,
            duration_ms
        )

        success, message = game_session.save()

        if not success:
            return jsonify({
                'success': False,
                'message': t(message, lang)
            }), 400

        # =========================
        # IAN -> GameResult
        # =========================

        from app.database import get_connection

        user_id = None

        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:

                cursor.execute(
                    "SELECT id FROM users WHERE username = %s",
                    (username,)
                )

                user_db = cursor.fetchone()

                if user_db:
                    user_id = user_db['id']

        if not user_id:
            return jsonify({
                'success': False,
                'message': 'Error: Usuari no trobat a la base de dades'
            }), 404

        resultat = GameResult(
            user_id=user_id,
            game_slug=game_id,
            score=score,
            duration_ms=duration_ms,
            details=details
        )

        if not resultat.save():
            return jsonify({
                'success': False,
                'message': 'Error en guardar GameResult'
            }), 500

        return jsonify({
            'success': True,
            'message': t('game_saved_successfully', lang)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


# =====================================================================
# RUTES GABRIEL (MONGODB)
# =====================================================================

@api_bp.route('/events', methods=['POST'])
def api_events():

    data = request.get_json()
    lang = session.get('lang', 'en')

    if not data:
        return jsonify({
            'success': False,
            'message': t('no_data_received', lang)
        }), 400

    try:

        event = GameEvent(
            data.get('game_id'),
            session.get('username', 'guest'),
            data.get('event_type'),
            data.get('data', {})
        )

        event_id = event.save_to_mongo()

        return jsonify({
            'success': True,
            'event_id': str(event_id)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@api_bp.route('/states', methods=['POST'])
def api_states():

    data = request.get_json()
    lang = session.get('lang', 'en')

    if not data:
        return jsonify({
            'success': False,
            'message': t('no_data_received', lang)
        }), 400

    try:

        state = GameState(
            data.get('game_id'),
            session.get('username', 'guest'),
            data.get('state_data', {})
        )

        state_id = state.save_to_mongo()

        return jsonify({
            'success': True,
            'state_id': str(state_id)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@api_bp.route('/logs/start', methods=['POST'])
def api_logs_start():

    data = request.get_json() or {}

    session_id = data.get('session_id') or str(uuid.uuid4())

    try:

        log = GameLog(
            data.get('game_id'),
            session.get('username', 'guest'),
            session_id
        )

        log.save_to_mongo()

        return jsonify({
            'success': True,
            'session_id': session_id
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@api_bp.route('/logs/end', methods=['POST'])
def api_logs_end():

    data = request.get_json()
    lang = session.get('lang', 'en')

    if not data:
        return jsonify({
            'success': False,
            'message': t('no_data_received', lang)
        }), 400

    session_id = data.get('session_id')

    if not session_id:
        return jsonify({
            'success': False,
            'message': t('session_id_required', lang)
        }), 400

    try:

        log = GameLog(
            data.get('game_id'),
            session.get('username', 'guest'),
            session_id
        )

        log.close_log(data.get('final_score'))
        log.save_to_mongo()

        return jsonify({
            'success': True,
            'session_id': session_id
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500