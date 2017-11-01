from app import db

class Data(db.Model):
	__tablename__ = "data"

	id = db.Column(db.Integer, primary_key=True)
	org_id = db.Column(db.String(64), db.ForeignKey('organizations.id'))
	data = db.Column(db.TEXT)

	def __init__(self, initial_data):
		for k, v in initial_data.items():
			setattr(self, k, v)

	def as_dict(self):
		return {
			"id": self.id,
			"org_id": self.org_id,
			"data": self.item
		}

	def __repr__(self):
		return """{"type": "Data", "id": %s }""" % self.id
