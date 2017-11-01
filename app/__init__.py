from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy


from sqlalchemy import event
import os

from config import config

db = SQLAlchemy()

def create_app(config_name):
	app = Flask(__name__)

	with app.app_context():
		app.config.from_object(config.get(config_name))
		app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

		config[config_name].init_app(app)

		@app.before_request
		def log_request():
			current_app.logger.debug(request.path)
			current_app.logger.debug(request.headers)

		db.init_app(app)

		from .main import main as main_blueprint
		app.register_blueprint(main_blueprint)

		from .dashboard import dashboard as dashboard_blueprint
		app.register_blueprint(dashboard_blueprint, url_prefix='/dashboard')

		return app