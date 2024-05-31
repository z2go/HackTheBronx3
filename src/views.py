from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from .models import Event
from . import db

views = Blueprint('views', __name__)

#So that all html files can access the username if logged in
@views.context_processor
def inject_user():
    return dict(userName=current_user.first_name if current_user.is_authenticated else None)


@views.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html")

#TODO THESE PAGES
@views.route("/events", methods=['GET','POST'])
#@login_required
def events():
    if request.method == 'POST':
        event_title = request.form.get('eventTitle')
        event_description = request.form.get('eventDescription')

        new_event = Event(event_title,event_description)
        db.session.add(new_event)
        db.session.commit(new_event)

    if request.method == 'GET':
        events = Event.query().all()

        
        

    return render_template("events.html")

@views.route('/network', methods=['GET'])
@login_required
def network():
    return render_template("network.html", user=current_user)

@views.route('/notifications', methods=['GET'])
#@login_required
def notifications():
    return render_template("notifications.html", user=current_user)

@views.route('/explore_jobs', methods=['GET'])
#@login_required
def explore_jobs():
    return render_template("explore_jobs.html", user=current_user)

@views.route('/settings', methods=['GET', 'POST'])
#@login_required
def settings():
    if request.method == 'POST':
        pass
    return render_template("settings.html", user=current_user)
