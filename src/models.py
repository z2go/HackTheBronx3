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

    def __init__(self, title, description, time_hours, time_minutes, pay, skills):
        self.title = title
        self.description = description
        self.time_hours = time_hours
        self.time_minutes = time_minutes
        self.pay = pay
        self.skills = skills

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.String(5000))
    creator = db.Column(db.String(150), default=current_user)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    date_happening = db.Integer()
    
    def __init__(self, title, description, creator, date_happening):
        self.title = title
        self.description = description
        self.creator = creator
        self.date_happening = date_happening

class Resume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    First_Name = db.Column(db.String)
    Last_Name = db.Column(db.String)
    Resume_Description = db.Column(db.String)
    Resume_Skills = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    def __init__(self, First_Name, Last_Name, Resume_Description, Resume_Skills):
        self.First_Name = First_Name
        self.Last_Name = Last_Name
        self.Resume_Description = Resume_Description
        self.Resume_Skills = Resume_Skills

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    interests = db.Column(db.String(1000))  
    location = db.Column(db.String(250))    
    about_me = db.Column(db.String(1000))   

    messages = db.relationship("Message")
    jobs = db.relationship("Job")

    def __init__(self, email, first_name, password, interests="", location="", about_me=""):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.interests = interests
        self.location = location
        self.about_me = about_me
