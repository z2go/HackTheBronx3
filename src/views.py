from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import Event, Job
from . import db

views = Blueprint('views', __name__)

#So that all html files can access the username if logged in
@views.context_processor
def inject_user():
    return dict(userName=current_user.first_name if current_user.is_authenticated else None)

@views.route('/upload_job', methods=['POST'])
@login_required
def upload_job():
    title = request.form.get('Task_Title')
    description = request.form.get('Task_Description')
    time_hours = request.form.get('Task_Time_Hours')
    time_minutes = request.form.get('Task_Time_Minutes')
    pay = request.form.get('Task_Pay')
    skills = request.form.get('Task_Skills')
    
    new_job = Job(
        title=title, 
        description=description, 
        time_hours=int(time_hours), 
        time_minutes=int(time_minutes), 
        pay=float(pay), 
        skills=skills, 
        user_id=current_user.id
    )
    db.session.add(new_job)
    db.session.commit()
    
    return redirect(url_for('views.explore_jobs'))

@views.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html")

@views.route('/upload_event',methods=['POST'])
@login_required
def upload_event():
    event_title = request.form.get('eventTitle')
    event_description = request.form.get('eventDescription')

    new_event = Event(event_title,event_description)
    db.session.add(new_event)
    db.session.commit()

#TODO THESE PAGES
@views.route("/events", methods=['GET','POST'])
#@login_required
def events():
    if request.method == 'GET':
        events = Event.query.all()

        
        

    return render_template("events.html")

@views.route('/network', methods=['GET'])
@login_required
def network():
    return render_template("network.html")

@views.route('/notifications', methods=['GET'])
#@login_required
def notifications():
    return render_template("notifications.html")

@views.route('/explore_jobs', methods=['GET'])
#@login_required
def explore_jobs():
    jobs = Job.query.all()
    return render_template('explore_jobs.html', jobs=jobs)

@views.route('/settings', methods=['GET', 'POST'])
#@login_required
def settings():
    if request.method == 'POST':
        pass
    return render_template("settings.html")
