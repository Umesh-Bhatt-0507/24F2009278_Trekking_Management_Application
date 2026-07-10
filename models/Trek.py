from extension import db
from datetime import datetime
class Trek(db.Model):
    __tablename__="treks"
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"))
    name=db.Column(db.String(200),nullable=False)
    location=db.Column(db.String(100),nullable=False)
    difficulty=db.Column(db.Integer,nullable=False)
    duration=db.Column(db.Integer,nullable=False)
    available_slots=db.Column(db.Integer,nullable=False)
    start_date=db.Column(db.DateTime,nullable=False)
    end_date=db.Column(db.DateTime,nullable=False)
    status=db.Column(db.String(20),nullable=False,default="open")  #pending // open// closed// completed
    description=db.Column(db.String(500))
    user=db.relationship("User",backref="treks")