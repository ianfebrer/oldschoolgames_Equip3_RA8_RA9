from flask import render_template, Blueprint, request, jsonify
from app.models.game import Game
from app.models.game_session import GameSession

games_bp = Blueprint('games', __name__, url_prefix='/games')

@games_bp.route('/pong')
def pong():
	return render_template('pong.html')

@games_bp.route('/trexpres')
def trexpres():
	return render_template('trexpres.html')

@games_bp.route('/atencioflash')
def atencioflash():
	return render_template('atencioflash.html')


