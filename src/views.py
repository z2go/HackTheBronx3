from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

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
@views.route("/events")
#@login_required
def events():
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
