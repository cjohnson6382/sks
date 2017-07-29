from flask import request, current_app, jsonify

# from flask_permissions import user_is
# from ..decorators import requires_auth, validate_body

import json

from . import main
from .. import db


@main.route('/dashboard', methods=["GET"])
# @user_is("admin")
def get_dashboard():
	return "returns the dashboard"

@main.route("/inspection-json", methods=["GET"])
def get_inspection():
	return jsonify(
		[
			{ "name": "derpy", "type": "picker", "options": ["derp", "wow", "fancy"], "default": "derp" }, 
			{ "name": "texty", "type": "textInput", "placeholder": "enter some text" }
		]
	)