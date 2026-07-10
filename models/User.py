from extension import db
from datetime import datetime

class User(db.Model):
    __tablename__="users"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(200),unique=True,nullable=False)
    password=db.Column(db.String(255),nullable=False)
    role=db.Column(db.String(20),nullable=False,default="user") #user admin staff 
    status=db.Column(db.String(20),nullable=False) # pending approved blacklisted
    created_at=db.Column(db.DateTime,default=datetime.utcnow)