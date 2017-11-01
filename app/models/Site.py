from app import db

class Site(db.Model):
	__tablename__ = "sites"

	id = db.Column(db.Integer, primary_key=True)
	org_id = db.Column(db.String(64), db.ForeignKey('organizations.id'))
	name = db.Column(db.String(64))
	street_number = db.Column(db.String(64))
	street_name= db.Column(db.String(64))
	city = db.Column(db.String(64))
	state = db.Column(db.String(64))
	country = db.Column(db.String(64))
	phone = db.Column(db.String(64))
	email = db.Column(db.String(64))

	def __init__(self, initial_data):
		for k, v in initial_data.items():
			setattr(self, k, v)

	def as_dict(self):
		return {
			"id": self.id,
			"org_id": self.org_id,
			"name": self.name,
			"street_number": self.street_number,
			"street_name": self.street_name,
			"city": self.city,
			"state": self.state,
			"country": self.country,
			"phone": self.phone,
			"email": self.email
		}

	def __repr__(self):
		return """{"type": "Site", "id": %s, "name": %s }""" % (self.id, self.name)
