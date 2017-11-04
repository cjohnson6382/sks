from app import db
from sqlalchemy.orm import relationship, backref


def model_type_getter(model_type):
	for model in db.Model._decl_class_registry.values():
		if hasattr(model, '__tablename__') and model.__tablename__ == model_type:
			return model

class Assigned(db.Model):
	__tablename__ = "assigned"

	id = db.Column(db.Integer, primary_key=True)
	org_id = db.Column(db.String(64), db.ForeignKey('organizations.id'))

	contractors = relationship("Contractor", secondary="assignedcontractors", backref=db.backref('contractors', lazy='dynamic'))
	inspections = relationship("Inspection", secondary="assignedinspections", backref=db.backref('inspections', lazy='dynamic'))
	sites = relationship("Site", secondary="assignedsites", backref=db.backref('sites', lazy='dynamic'))

	def __init__(self, initial_data):
		attributes_to_remove = []
		with db.session.no_autoflush:
			for k, v in initial_data.items(): 
				if type(v) == list:
					model_type = model_type_getter(k)
					setattr(self, k, db.session.query(model_type).filter(model_type.id.in_(initial_data[k])).all())
					attributes_to_remove.append(k)

			initial_data = {k: v for k, v in initial_data.items() if k not in attributes_to_remove}

		for k, v in initial_data.items():
			setattr(self, k, v)

	def as_dict(self):
		return {
			"id": self.id,
			"org_id": self.org_id,
			"contractors": [a.name_first + " " + a.name_last for a in self.contractors],
			"inspections": [a.name for a in self.inspections],
			"sites": [a.name for a in self.sites]
		}

	def __repr__(self): return """{"type": "Assignment", "id": %s }""" % self.id
