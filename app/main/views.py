from flask import render_template, redirect, url_for, abort, flash, request, current_app, make_response, send_from_directory, jsonify
from flask_login import login_required, current_user
from flask_restful.utils import cors
from flask_cors import cross_origin

from ..decorators import requires_auth, validate_body

import json

from . import main
from .. import db


@main.route('/dashboard', methods=["GET"])
@user_is("admin")
def get_dashboard():
	return "returns the dashboard"
