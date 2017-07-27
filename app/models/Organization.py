from app import db
from sqlalchemy import Column, String, ForeignKey
import uuid
import json

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref

from flask.ext.permissions.models import UserMixin

class User(UserMixin):
	__tablename__ = "organizations"

	id = db.Column(db.String(64), ForeignKey('roleholders.id'), primary_key=True)
	name = db.Column(db.String(128))
	item = db.Column(JSONB)

	def __init__(self, initial_data):
		self.id = uuid.uuid1().hex
		for k, v in initial_data.items():
			setattr(self, k, v)

	def as_dict(self):
		return {
			"id": self.id,
			"name": self.name,
			"item": self.item
		}

	def __repr__(self):
		return """{"type": "Organization", "id": %s }""" % self.id
