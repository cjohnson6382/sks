from app import db

assignedcontractors = db.Table(
	"assignedcontractors",
	db.Column("left_id", db.String(64), db.ForeignKey("assigned.id"), primary_key=True),
	db.Column("right_id", db.String(64), db.ForeignKey("contractors.id"), primary_key=True)
)

assignedsites = db.Table(
	"assignedsites",
	db.Column("left_id", db.String(64), db.ForeignKey("assigned.id"), primary_key=True),
	db.Column("right_id", db.String(64), db.ForeignKey("sites.id"), primary_key=True)
)

assignedinspections = db.Table(
	"assignedinspections",
	db.Column("left_id", db.String(64), db.ForeignKey("assigned.id"), primary_key=True),
	db.Column("right_id", db.String(64), db.ForeignKey("inspections.id"), primary_key=True)
)