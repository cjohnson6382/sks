import jwt

import urllib.request
import json
import jsonschema

from jose import jwk
from jose import jws

from functools import wraps
from flask import request, jsonify, _app_ctx_stack, current_app
from flask_cors import cross_origin

from app import db
from app.models import User, Organization
# from app.utils.utilities import method_dict

# from app.functions.apps import auth_whitelist

from config import config

auth0_url = config.get("development").AUTH0_URL


def has_permissions(permission_level):
	# @wraps(f)
	def wrap (f):
		def decorated(*args, **kwargs):
			u = User.query.filter_by(sub_id=_app_ctx_stack.top.current_user.get('sub')).first()
			if not u.permissions >= permission_level:
				return handle_error({
					'code': 'cannot subscribe to functions',
					'description': 'you do not have permission to create or modify resources for your organization'
				}, 400)

			return f(*args, **kwargs)
		return decorated
	return wrap


def handle_error(error, status_code):
		resp = jsonify(error)
		resp.status_code = status_code
		return resp


def prepare_event(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		# print(request.args.get("filter"), request.args.get("constraint"))

		if request.method == "GET": _app_ctx_stack.top.event = request.args
		if request.method == "POST" or request.method == "PUT": _app_ctx_stack.top.event = request.get_json()

		return f(*args, **kwargs)

	return decorated


"""
		This is what a decoded auth token looks like:
		('_app_ctx_stack.top.current_user: ', {
				u'iss': u'https://cjohnson6382.auth0.com/',
				u'iat': 1484031557,
				u'sub': u'auth0|58702f50ef793e559a07c56d',
				u'exp': 1484067557,
				u'aud': u'01TFwGUcUScthq1bPqjiF4Z4rKxd2zU7'
		})
"""

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		#	the auth0_url gets the public key for our auth0 domain
		#		https://cjohnson6382.auth0.com/.well-known/jwks.json
		resp = urllib.request.urlopen(auth0_url)
		data = json.loads(resp.read().decode('utf-8'))

		#	get the access_token that the client sent with their request
		auth = request.headers.get('Authorization', None)

		#	if there is no access_token, or if the token is improperly formatted, error out
		if not auth:
				return handle_error({
						'code': 'authorization_header_missing',
						'description': 'Authorization header is expected'
				}, 401)

		#	auth is in the format 'Bearer <Access_Token>'
		parts = auth.split()

		if parts[0].lower() != 'bearer':
				return handle_error({
						'code': 'invalid_header',
						'description':'Authorization header must start with Bearer'
				}, 401)
		elif len(parts) == 1:
				return handle_error({
						'code': 'invalid_header',
						'description': 'Token not found'
				}, 401)
		elif len(parts) > 2:
				return handle_error({
						'code': 'invalid_header',
						'description': 'Authorization header must be Bearer + \s + token'
				}, 401)

		#	get the access_token portion of auth
		token = parts[1]

		#	use the auth0 public key to decode the access_token that was encrypted with the user's key on the client side
		#		error out if decryption does not work for one reason or another
		try:
				payload = jws.verify(
						token,
						data,
						algorithms='[RS256]'
				)
		except jwt.ExpiredSignature:
				return handle_error({
						'code': 'token_expired',
						'description': 'token is expired'
				}, 401)
		except jwt.InvalidAudienceError:
				return handle_error({
						'code': 'invalid_audience',
						'description': 'incorrect audience, expected: ' + client_id
				}, 401)
		except jwt.DecodeError:
				return handle_error({
						'code': 'token_invalid_signature',
						'description': 'token signature is invalid'
				}, 401)
		except Exception as e:
				return handle_error({
						'code': 'invalid_header',
						'description': 'Unable to parse authentication token. %r' % e
				}, 400)

		user = json.loads(payload.decode())

		################################################################################
		#	this is for development; it creates a user in the database 
		#		if that user has an auth0 account but no DB representation yet
		################################################################################
		o = Organization.query.first()
		u = User.query.filter(User.sub_id == user.get("sub")).first()
		if not u: 
			u = User({ "permissions": 5, "name": "auto-created user", "sub_id": user.get("sub"), "org_id": o.id })
			db.session.add(u)
			db.session.commit()
		################################################################################



		#	add the decrypted contents of the token to the server app's state so that it is available
		#		to any functions down the request-processing pipeline
		#		(see the format of the token just above this function definition)
		_app_ctx_stack.top.current_user = user
		return f(*args, **kwargs)

	return decorated



# def api_validate_body(f):
# 	@wraps(f)
# 	def decorated(*args, **kwargs):
# 		if not (request.method == "POST" or request.method == "PUT"): 
# 			return f(*args, **kwargs)

# 		body = request.get_json()
# 		if not body:
# 			return handle_error({
# 				'code': 'request contains no JSON body',
# 				'description': 'POST/PUT body must include a JSON object'
# 			}, 400)
		
# 		method = App.query.filter(App.name == method_dict.get(request.method)).first()
# 		resource = App.query.filter(App.name == request.path.split("/")[-1].lower()).first()

# 		schemas = [Schema.query.get(s) for s in method.schemas + resource.schemas]

# 		try:
# 			[jsonschema.validate(body, schema.value) for schema in schemas]

# 		except Exception as e:
# 			print("validation failed for request body %r, using schemas %r with error %r" % (body, schemas, e))
# 			return handle_error({
# 				'code': 'Validation Failed',
# 				'description': 'event %r failed to validate using schemas %r: %r' % (body, schemas, e)
# 			}, 400)	

# 		return f(*args, **kwargs)

# 	return decorated


# def validate_body(f):
# 	@wraps(f)
# 	def decorated(*args, **kwargs):
# 		if not (request.method == "POST" or request.method == "PUT"): 
# 			return f(*args, **kwargs)

# 		body = request.get_json()
# 		if not body:
# 			return handle_error({
# 				'code': 'request contains no JSON body',
# 				'description': 'POST/PUT body must include a JSON object'
# 			}, 400)
		
# 		print("request path; in validate_body decorator: ", request_path)

# 		route = Schema.query.filter(Schema.name == request.path).first()
# 		try:
# 			[jsonschema.validate(j, schema) for schema in route.get("schemas")]
# 			return f(*args, **kwargs)

# 		except Exception as e:
# 			return handle_error({
# 				'code': 'Validation Failed',
# 				'description': 'event %r failed to validate using schema %r: %r' % (body, route.get("schemas"), e)
# 			}, 400)	

# 	return decorated

