from app import db
from sqlalchemy import Column, String, ForeignKey
import uuid
import json

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, backref

class Inspection():
	__tablename__ = "inspections"

	id = db.Column(db.String(64), ForeignKey('roleholders.id'), primary_key=True)
	org_id = db.Column(db.String(64), ForeignKey('organizations.id'))
	description = db.Column(db.Text())
	item = db.Column(JSONB)

	def __init__(self, initial_data):
		# super().__init__()
		self.id = uuid.uuid1().hex
		for k, v in initial_data.items():
			setattr(self, k, v)

	def as_dict(self):
		return {
			"id": self.id,
			"org_id": self.org_id,
			"description": self.description,
			"item": self.item
		}

	def __repr__(self):
		return """{"type": "Inspection", "id": %s }""" % self.id
