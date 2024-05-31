from . import db
from flask_login import UserMixin, current_user
from sqlalchemy.sql import func


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(5000), nullable=False)
    time_hours = db.Column(db.Integer, nullable=False)
    time_minutes = db.Column(db.Integer, nullable=False)
    pay = db.Column(db.Float, nullable=False)
    skills = db.Column(db.String(2000), nullable=False)
    posted_date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, title, description, time_hours, time_minutes, pay, skills, user_id):
        self.title = title
        self.description = description
        self.time_hours = time_hours
        self.time_minutes = time_minutes
        self.pay = pay
        self.skills = skills
        self.user_id = user_id

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(5000))
    creator = db.Column(db.String(150), default=current_user)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    
    def __init__(self, title, description):
        self.title = title
        self.description = description
        

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    about_me = db.Column(db.String(20000), default="")
    
    
    messages = db.relationship("Message")

    def __init__(self, email, first_name, password):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.about_me = "I like cheese"
