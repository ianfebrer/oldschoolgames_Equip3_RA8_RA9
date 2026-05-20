import os

from dotenv import load_dotenv
from flask import Flask

def create_app():
	load_dotenv()

	app = Flask(__name__)
	app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'canviar')
	app.config['TEMPLATES_AUTO_RELOAD'] = True

	@app.after_request
	def add_header(response):
		response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
		response.headers['Pragma'] = 'no-cache'
		response.headers['Expires'] = '-1'
		return response

	from app.routes.auth import auth_bp
	from app.routes.main import main_bp
	from app.routes.games import games_bp
	from app.routes.api import api_bp


	app.register_blueprint(auth_bp)
	app.register_blueprint(main_bp)
	app.register_blueprint(games_bp)
	app.register_blueprint(api_bp)

	from app.translations import t
	from flask import session

	@app.context_processor
	def inject_translations():
		lang = session.get('lang', 'en')
		return dict(t=lambda key: t(key, lang), current_lang=lang)

	return app
