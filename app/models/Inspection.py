from app import db

class Inspection(db.Model):
	__tablename__ = "inspections"

	id = db.Column(db.Integer, primary_key=True)
	org_id = db.Column(db.String(64), db.ForeignKey('organizations.id'))
	description = db.Column(db.Text())
	item = db.Column(db.TEXT)

	def __init__(self, initial_data):
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
