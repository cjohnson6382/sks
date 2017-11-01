from app import db

class Completed(db.Model):
	__tablename__ = "completed"

	id = db.Column(db.Integer, primary_key=True)
	org_id = db.Column(db.String(64), db.ForeignKey('organizations.id'))
	contractor = db.Column(db.String(64), db.ForeignKey("contractors.id"))
	inspection = db.Column(db.String(64), db.ForeignKey("inspections.id"))
	data = db.Column(db.TEXT)


	def __init__(self, initial_data):
		for k, v in initial_data.items():
			setattr(self, k, v)

	def as_dict(self):
		return {
			"id": self.id,
			"org_id": self.org_id,
			"contractor": self.contractor,
			"inspection": self.inspection,
			"data": self.data
		}

	def __repr__(self):
		return """{
			"type": "Completed", 
			"id": %s, 
			"org_id": %s, 
			"contractor": %s, 
			"inspection": %s 
		}""" % (self.id, self.org_id, self.contractor, self.inspection)
