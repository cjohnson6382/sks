from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy

from flask.ext.permissions.core import Permissions


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

		# I have no idea what this does right now...
		perms = Permissions(app, db, current_user)

		from .main import main as main_blueprint
		app.register_blueprint(main_blueprint)

		# from .api_1_0 import api_bp as api_1_0_blueprint
		# app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

		return app