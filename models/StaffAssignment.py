from extension import db
from datetime import datetime

class StaffAssignment(db.Model):
    __tablename__="staff_assignments"
    id=db.Column(db.Integer,primary_key=True)
    staff_id=db.Column(db.Integer,db.ForeignKey("users.id"))
    trek_id=db.Column(db.Integer,db.ForeignKey("treks.id"))
    assigned_date=db.Column(db.DateTime,default=datetime.utcnow)
    staff=db.relationship("User",backref="assignments")
    trek=db.relationship("Trek",backref="assignments")