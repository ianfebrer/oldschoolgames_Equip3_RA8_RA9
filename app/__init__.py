from flask import Flask

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'canviar'

	from app.routes.auth import auth_bp
	from app.routes.main import main_bp
	from app.routes.games import games_bp

	app.register_blueprint(auth_bp)
	app.register_blueprint(main_bp)
	app.register_blueprint(games_bp)

	return app
