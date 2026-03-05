from flask import Flask

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'canviar'

	from app.routes.auth import auth_bp
	from app.routes.main import main_bp
	from app.routes.games import games_bp
	from app.routes.api import api_bp


	app.register_blueprint(auth_bp)
	app.register_blueprint(main_bp)
	app.register_blueprint(games_bp)
	app.register_blueprint(api_bp)

	return app
