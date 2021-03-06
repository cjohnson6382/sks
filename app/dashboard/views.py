from flask import request, jsonify, _app_ctx_stack, current_app

# from flask_permissions import user_is
from functools import wraps

import json

from . import dashboard
from .. import db

from app.models import User, Organization, Data, Learning, Inspection, Contractor, Assigned, Site

from app.decorators import requires_auth, prepare_event
from flask_cors import cross_origin

models_dict = {
	"data": Data,
	"inspections": Inspection,
	"learning": Learning,
	"contractors": Contractor,
	"sites": Site,
	"assign": Assigned
}

# def create_inspection (inspection):
# 	inspection["inspection"] = json.dumps(inspection["inspection"])
# 	i = Inspection(inspection)
# 	db.session.add(i)
# 	db.session.commit()

# def create_assignment (assignment):
# 	a = Assigned(assignment)
# 	db.session.add(a)
# 	db.session.commit()
# 	return a.as_dict()


# @dashboard.route('/', defaults={"route": ""})
@dashboard.route('/<string:route>', methods=["GET"])
@cross_origin()
@requires_auth
@prepare_event
def get (route):
	u = User.query.filter(User.sub_id == _app_ctx_stack.top.current_user.get("sub")).first()

	M = models_dict[route]
	result = M.query.filter(M.org_id == u.org_id).all()
	return jsonify([r.as_dict() for r in result])

@dashboard.route('/<string:route>/<string:id>', methods=["GET"])
@cross_origin()
@requires_auth
@prepare_event
def get_one (route, resource_id):
	u = User.query.filter(User.sub_id == _app_ctx_stack.top.current_user.get("sub")).first()

	M = models_dict[route]
	result = M.query.get(resource_id)
	return jsonify(result.as_dict())

# @dashboard.route('/', defaults={"route": ""})
@dashboard.route('/<string:route>', methods=["POST"])
@cross_origin()
@requires_auth
@prepare_event
def post (route):
	M = models_dict[route]
	u = User.query.filter(User.sub_id == _app_ctx_stack.top.current_user.get("sub")).first()
	a = { **_app_ctx_stack.top.event, "org_id": u.org_id }

	for k, v in a.items():
		if isinstance(v, dict) or isinstance(v, list):
			a[k] = json.dumps(v)

	m = M(a)
	db.session.add(m)
	db.session.commit()

	return jsonify(m.as_dict())


# @dashboard.route('/data_analysis', methods=["GET"])
# @requires_auth
# @cross_origin()
# def data_analysis ():
# 	u = User.query.filter(User.sub = _app_ctx_stack.top.current_user.get("sub")).first()
# 	dd = Data.query.filter(Data.org_id == u.org_id).all()
# 	return jsonify([d.as_dict() for d in dd])

# @dashboard.route('/get_inspections', methods=["GET"])
# @requires_auth
# @cross_origin()
# def inspections ():
# 	u = User.query.filter(User.sub = _app_ctx_stack.top.current_user.get("sub")).first()

# 	return jsonify()

# @dashboard.route('/get_contractors', methods=["GET"])
# @requires_auth
# @cross_origin()
# def contracts ():
# 	u = User.query.filter(User.sub = _app_ctx_stack.top.current_user.get("sub")).first()
# 	return jsonify()

# @dashboard.route('/get_sites', methods=["GET"])
# @requires_auth
# @cross_origin()
# def sites ():
# 	u = User.query.filter(User.sub = _app_ctx_stack.top.current_user.get("sub")).first()
# 	return jsonify()

# @dashboard.route('/assign_inspections', methods=["POST"])
# @requires_auth
# @cross_origin()
# def assign ():
# 	u = User.query.filter(User.sub = _app_ctx_stack.top.current_user.get("sub")).first()
# 	f = request.get_json()
# 	return jsonify()

# @dashboard.route('/learning', methods=["GET"])
# @requires_auth
# @cross_origin()
# def learning ():
# 	u = User.query.filter(User.sub = _app_ctx_stack.top.current_user.get("sub")).first()
# 	return jsonify()
