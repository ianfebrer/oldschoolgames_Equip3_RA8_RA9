from flask import render_template, Blueprint, session

games_bp = Blueprint('games', __name__, url_prefix='/games')

@games_bp.route('/pong')
def pong():
	return render_template('pong.html', username=session.get('username'))

@games_bp.route('/trexpres')
def trexpres():
	return render_template('trexpres.html', username=session.get('username'))

@games_bp.route('/memory')
def atencioflash():
	return render_template('memory.html', username=session.get('username'))
