from app import db

class Assigned():
	__tablename__ = "assigned"

	id = db.Column(db.Integer, primary_key=True)
	org_id = db.Column(db.String(64), db.ForeignKey('organizations.id'))
	contractor = db.Column(db.String(64), db.ForeignKey("contractors.id"))
	inspection = db.Column(db.String(64), db.ForeignKey("inspections.id"))

	def __init__(self, initial_data):
		for k, v in initial_data.items():
			setattr(self, k, v)

	def as_dict(self):
		return {
			"id": self.id,
			"org_id": self.org_id,
			"name_first": self.description,
			"name_last": self.item,
			"street_number": self.street_number,
			"street_name": self.street_name,
			"city": self.city,
			"state": self.state,
			"country": self.country,
			"phone": self.phone,
			"email": self.email
		}

	def __repr__(self):
		return """{"type": "Contractor", "id": %s, "firstname": %s }""" % (self.id, self.name_first)
