
import unittest
import json
import jsonschema
import requests

from flask import current_app
from app import create_app, db

# https://github.com/raddevon/flask-permissions
 from flask.ext.permissions.core import Permissions
 from flask.ext.permissions.models import UserMixin, Role

from app.main.views import dashboard

from tests.utilities import dummy_inspection

# from app.utils.test_schemas import test_schemas

# from random import randint
# import forgery_py

# from app.models import App, Asset, Organization, Role, Schema, Site, Transaction, User, Grant, Point, Function
from app.models import Inspection, User, Organization

class TestModels(unittest.TestCase):
	def setUp(self):
			self.app = create_app('testing')
			self.app_context = self.app.app_context()
			self.app_context.push()
			db.create_all()

			self.client = self.app.test_client()

			self._routes = dict()

	def tearDown(self):

		db.session.remove()
		db.drop_all()

		self.app_context.pop()

	def test_01_organization(self):
		o = Organization({})
		db.session.add(o)
		db.session.commit()

		#	what does an organization do in this app?

	"""
	my preferred way of doing permissions here might not work; I need to figure out how 'current_user' works 
		because that's what permissions uses to check roles
	"""
	def test_02_user(self):
		role = Role("admin")
		role.add_abilities("add_user", "delete_user")

		db.session.add(role)
		db.session.commit()

		#	User subclasses the UserMixin from flask-permissions
		u = User()

		u.add_roles("admin")

		db.session.add(u)
		db.session.commit()

		r = self.app.post('/dashboard', data={}, follow_redirects=True)
		self.assertEqual(r.status_code, 200)

		user.remove_roles("admin")

		db.session.add(u)
		db.session.commit()

		#	this should fail because user does not have permission to access this route now
		r = self.app.post('/dashboard', data={}, follow_redirects=True)
		self.assertEqual(r.status_code, 401)


	def test_03_inspection(self):
		i = Inspection(dummy_inspection)

		db.session.add(i)
		db.session.commt()

		inspection = Inspection.query.get(i.id)

		i_jsonb = inspection.item
		i_dict = json.loads(i_jsonb)
		self.assertTrue(isinstance(i_dict, dict))
		self.assertIsNotNone(inspection._created)

