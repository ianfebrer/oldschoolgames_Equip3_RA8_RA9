from flask import render_template, Blueprint, session, jsonify, request
from app.models.game_session import GameSession
from app.models.game import Game

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
	username = session.get('username')
	selected_game = request.args.get('game', 'pong')

	jocs = Game.get_all_main()
	leaderboard = GameSession.get_leaderboard(selected_game)

	return render_template('index.html', username=username, leaderboard=leaderboard, jocs=jocs, selected_game=selected_game)
