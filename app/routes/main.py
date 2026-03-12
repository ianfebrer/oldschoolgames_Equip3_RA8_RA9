from flask import render_template, Blueprint, session, jsonify, request
from app.models.game_session import GameSession

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
	username = session.get('username')
	selected_game = request.args.get('game', 'pong')

	jocs = [
		{'id': 'pong', 'name': 'Pong'},
		{'id': 'trexpres', 'name': 'Trexpres'},
		{'id': 'memory', 'name': 'Memory'},
	]

	sessions = GameSession(None, None, None, None, None).get_all()

	sessions_filtrades = [
		s for s in sessions
		if s.get('game_id') == selected_game
	]

	millors_per_jugador = {}
	for s in sessions_filtrades:
		user = s.get('username')
		score = s.get('score', 0)
		if user not in millors_per_jugador or score > millors_per_jugador[user]['score']:
			millors_per_jugador[user] = s

	leaderboard = sorted(
		millors_per_jugador.values(),
		key=lambda s: s.get('score', 0),
		reverse=True
		)[:5]

	return render_template('index.html', username=username, leaderboard=leaderboard, jocs=jocs, selected_game=selected_game)
