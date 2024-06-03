from flask_login import current_user
from flask import Flask, request, session  
from flask_socketio import join_room, leave_room, send, SocketIO
from src import create_app

app = create_app()
#app = Flask(__name__)
app.config['SECRET KEY'] = 'yefwy'
socketio = SocketIO(app)

if __name__ == '__main__':
    socketio.run(app, debug=True, port="5000") 




