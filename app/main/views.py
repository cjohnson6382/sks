from flask import request, current_app, jsonify

# from flask_permissions import user_is
# from ..decorators import requires_auth, validate_body

import json

from . import main
from .. import db

inspections = {
	"base": [	
		{ "name": "general", "values": [{ "name": "pickerly", "type": "picker", "options": ["solar stuff", "some other stuff", "very official inspection"], "selected": "derp" }] },
		{ "name": "inverter", "values": [{ "name": "texty", "type": "textInput", "placeholder": "enter some text" }] }			
	]

	
}

@main.route('/dashboard', methods=["GET"])
# @user_is("admin")
def get_dashboard():
	return "returns the dashboard"

@main.route("/inspection-json/<id>", methods=["GET"])
def get_inspection():
	return jsonify(inspections[id])

@main.route("/inspections-list", methods=["GET"])
def get_inspections():
	keys = list(inspections.keys())
	print(keys)
	return jsonify(keys)

@main.route("/form", methods=["POST"])
def new_form():
	form_init = request.get_json()
	try: 
		return jsonify({"status": form_init, "message": "echoing user submission"})
		"""
		form = Form(form_init)
		db.session.add(form)
		db.session.commit()
		return jsonify({ "status": "successfully created form" })
		"""
	except Exception as e: 
		return jsonify({ "status": "failed to create form %s" % e })
