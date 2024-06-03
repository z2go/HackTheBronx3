from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session, Flask
from flask_login import login_required, current_user
# import socketio
from .models import Event, Job, Resume, User
from . import db
# from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase


import openai
import os
import json

views = Blueprint('views', __name__)


#So that all html files can access the these variables
@views.context_processor
def inject_user():
    maps_api_key = os.getenv('MAPS_API_KEY')
    openai_gpt_key = os.getenv('OPENAI_GPT_KEY')
    return dict(
        user=current_user if current_user.is_authenticated else None,
        maps_api_key=maps_api_key,
        openai_gpt_key=openai_gpt_key
    )

@views.route('/complete_account', methods=['POST'])
@login_required
def complete_account():
    interests = request.form.get('interests')
    location = request.form.get('location')
    about_me = request.form.get('about_me')

    current_user.interests = interests
    current_user.location = location
    current_user.about_me = about_me
    db.session.commit()

    return redirect(url_for('views.dashboard'))

@views.route('/upload_job', methods=['POST'])
# @login_required
def upload_job():
    title = request.form.get('Task_Title')
    description = request.form.get('Task_Description')
    time_hours = request.form.get('Task_Time_Hours')
    time_minutes = request.form.get('Task_Time_Minutes')
    pay = request.form.get('Task_Pay')
    skills = request.form.get('Task_Skills')
    location = request.form.get('job_location')
    eligibility_min = request.form.get('Eligibility_Min')
    eligibility_max = request.form.get('Eligibility_Max')
    event_creator = current_user.username

    new_job = Job(
        title=title,
        description=description,
        time_hours=int(time_hours),
        time_minutes=int(time_minutes),
        pay=float(pay),
        skills=skills,
        location=location,
        eligibility_min=int(eligibility_min),
        eligibility_max=int(eligibility_max),
        user_id=current_user.id,
        creator = event_creator 
    )
    db.session.add(new_job)
    db.session.commit()

    return redirect(url_for('views.explore_jobs'))

@views.route('/job/<int:job_id>', methods=['GET'])
def view_job(job_id):
    job = Job.query.get_or_404(job_id)
    return render_template('view_job.html', job=job)

@views.route('/upload_resume', methods=['POST'])
# @login_required
def upload_resume():
    First_Name = request.form.get('Resume_First_Name')
    Last_Name = request.form.get('Resume_Last_Name')
    Resume_Description = request.form.get('Resume_Description')
    Resume_Skills = request.form.get('Resume_Skills')
    event_creator = current_user.username
    ##TODO
    new_resume = Resume(
        First_Name=First_Name,
        Last_Name=Last_Name,
        Resume_Description=Resume_Description, 
        Resume_Skills=Resume_Skills, 
        user_id=current_user.id,
        creator = event_creator
    )
    db.session.add(new_resume)
    db.session.commit()

    return redirect(url_for('views.explore_resumes'))
    
@views.route('/upload_event',methods=['POST'])
# @login_required
def upload_event():
    event_title = request.form.get('eventTitle')
    event_description = request.form.get('eventDescription')
    event_creator = current_user.username
    event_date = request.form.get('eventDate')

    new_event = Event(event_title,event_description, event_creator, event_date)
    db.session.add(new_event)
    db.session.commit()
    return redirect(url_for('views.events'))

@views.route('/analyze_resume',methods=['POST'])
@login_required
def analyze_resume():
    print("ANALYZE REUSME")

##Page routing
@views.route("/")
@login_required
def dashboard():
    return render_template("dashboard.html")

@views.route("/events", methods=['GET','POST'])
@login_required
def events():
    events = Event.query.all()

    return render_template("events.html", events = events, current_user=current_user)

@views.route('/network', methods=['GET'])
@login_required
def network():
    return render_template("network.html", friends = db.session.query(User).all())

@views.route('/chat', methods=['GET','POST'])
@login_required
def chat():
    session.clear()
    room = create_new_code(4)
    rooms[room] = {'messages':[]}
    session["room"] = room
    session["name"] = current_user.username
    return render_template("chat.html")

rooms = {}
def create_new_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        if code not in rooms:
            break
        
# @socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    # send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")


@views.route('/notifications', methods=['GET'])
@login_required
def notifications():
    return render_template("notifications.html")

@views.route('/explore_jobs', methods=['GET'])
@login_required
def explore_jobs():
    jobs = Job.query.all()
    return render_template('explore_jobs.html', jobs=jobs)

@views.route('/find_job_matches', methods=['POST', 'GET'])
# @login_required
def find_job_matches():
    user = current_user
    jobs = Job.query.all()

    client = openai.OpenAI(api_key=os.getenv('OPENAI_GPT_KEY'))

    conversation = []
    prompt = f"User information:\nName: {user.username}\nInterests: {user.interests}\nLocation: {user.location}\n\nJobs available:\n"
    for job in jobs:
        prompt += f"Title: {job.title}\nDescription: {job.description}\nTime: {job.time_hours} hours {job.time_minutes} minutes\nPay: ${job.pay}\nSkills: {job.skills}\nEligibility: {job.eligibility_min} - {job.eligibility_max} years\nLocation: {job.location}\n\n"
    conversation.append({'role': 'system', 'content': prompt})
    conversation.append({'role': 'system', 'content': "\nPlease rank these jobs for the user based on their suitability."})

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=conversation,
        temperature=0,
        max_tokens=500
    )

    ranked_jobs = response.choices[0].message.content.strip().split('\n')
    print(ranked_jobs)

    return jsonify({"ranked_jobs": ranked_jobs})

@views.route('/explore_resumes', methods=['GET'])
@login_required
def explore_resumes():
    resumes = Resume.query.all()
    # print(resumes[0])
    return render_template('explore_resumes.html', resumes=resumes)

def convert_interests_to_readable(interests):
    list_of_maps = json.loads(interests)
    return ", ".join([item['value'] for item in list_of_maps])

def convert_readable_to_interests(readable_interests):
    list_of_maps = [{"value": item.strip()} for item in readable_interests.split(',')]
    return json.dumps(list_of_maps)

@views.route('/profile/<username>', methods=['GET', 'POST'])
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    is_current_user = (user.id == current_user.id)

    if request.method == 'POST' and is_current_user:
        user.username = request.form.get('first_name')
        user.location = request.form.get('location')
        user.interests = convert_readable_to_interests(request.form.get('interests'))
        user.about_me = request.form.get('about_me')
        db.session.commit()
        return redirect(url_for('views.profile', username=user.username))

    return render_template('profile.html', user=user, is_current_user=is_current_user, user_interests = convert_interests_to_readable(user.interests))

@views.route('/my_events',methods=['GET','POST'])
@login_required
def my_events():
    events = Event.query.all()

    return render_template("my_events.html", events = events, current_user=current_user)

@views.route('/remove_job/<int:job_id>', methods=['GET','POST'])
def remove_job(job_id):
    job = Job.query.get_or_404(job_id)

    db.session.delete(job)
    db.session.commit()

    jobs = Job.query.all()
    return redirect(url_for('views.explore_jobs'))

@views.route('/remove_resume/<int:resume_id>', methods=['GET','POST'])
def remove_resume(resume_id):
    resume = Resume.query.get_or_404(resume_id)

    db.session.delete(resume)
    db.session.commit()

    resumes = Resume.query.all()
    return redirect(url_for('views.explore_resumes'))

@views.route('/remove_event/<int:event_id>', methods=['GET','POST'])
def remove_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    db.session.delete(event)
    db.session.commit()

    events = Event.query.all()
    return redirect(url_for('views.events'))