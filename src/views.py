from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template("index.html", user=current_user, userName=current_user.first_name)

#TODO THESE PAGES
@views.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@views.route("/events")
@login_required
def events():
    return render_template("events.html")

@views.route('/friends', methods=['GET'])
@login_required
def friends():
    return render_template("friends.html", user=current_user)

@views.route('/notifications', methods=['GET'])
@login_required
def notifications():
    return render_template("notifications.html", user=current_user)

@views.route('/explore_jobs', methods=['GET'])
@login_required
def explore_jobs():
    return render_template("explore_jobs.html", user=current_user)

@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        pass
    return render_template("settings.html", user=current_user)
