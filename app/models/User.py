from app import db

class User(db.Model):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	org_id = db.Column(db.String(64), db.ForeignKey('organizations.id'))
	name = db.Column(db.String(128))
	item = db.Column(db.TEXT)
	sub_id = db.Column(db.String(128))

	def __init__(self, initial_data, roles=None):
		for k, v in initial_data.items():
			setattr(self, k, v)

	def as_dict(self):
		return {
			"id": self.id,
			"org_id": self.org_id,
			"name": self.name,
			"item": self.item
		}

	def __repr__(self):
		return """{"type": "User", "id": %s }""" % self.id
