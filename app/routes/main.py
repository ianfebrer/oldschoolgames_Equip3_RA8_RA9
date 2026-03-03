from flask import render_template, Blueprint, session

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
	username = session.get('username')
	return render_template('index.html', username=username)
