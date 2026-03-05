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

	leaderboard = sorted(
		sessions_filtrades,
		key=lambda s: s.get('score', 0),
		reverse=True
		)[:5]

	return render_template('index.html', username=username, leaderboard=leaderboard, jocs=jocs, selected_game=selected_game)
