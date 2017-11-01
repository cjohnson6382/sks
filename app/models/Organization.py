from app import db

from sqlalchemy.orm import relationship

class Organization(db.Model):
	__tablename__ = "organizations"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128))
	item = db.Column(db.TEXT)

	users = relationship("User", cascade="all, delete-orphan")

	def __init__(self, initial_data):
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
