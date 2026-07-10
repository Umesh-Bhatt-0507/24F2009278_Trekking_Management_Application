from extension import db
from datetime import datetime

class Booking(db.Model):
    __tablename__="bookings"
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey("users.id"))
    trek_id=db.Column(db.Integer,db.ForeignKey("treks.id"))
    booking_date=db.Column(db.DateTime,default=datetime.utcnow)
    status=db.Column(db.String(20),default="booked") #booked // cancelled // completed
    user=db.relationship("User",backref="bookings")
    trek=db.relationship("Trek",backref="bookings")
    __table_args__=(db.UniqueConstraint("user_id","trek_id"),)