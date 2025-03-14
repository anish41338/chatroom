from flask import Blueprint, render_template, request
from flask_socketio import emit, join_room, leave_room

# Blueprint for User 1
user1_bp = Blueprint('user2', __name__, url_prefix='/user2', template_folder='templates')

# Username for this blueprint
USERNAME = 'user2'

@user1_bp.route('/')
def index():
    return render_template('user.html', username=USERNAME)

# SocketIO event handlers specific to this user
@user1_bp.socketio.on('send_message')
def handle_send_message(data):
    recipient = data.get('recipient')
    message = data.get('message')
    if not recipient or not message:
        emit('error', {'message': 'Recipient and message are required'})
        return

    # Emit message to the recipient's room
    emit('receive_message', {
        'sender': USERNAME,
        'message': message
    }, room=recipient)

    # Send acknowledgment back to sender
    emit('acknowledge', {'message': f"Message sent to {recipient}: {message}"})

@user1_bp.socketio.on('join_user_room')
def handle_join_user_room():
    join_room(USERNAME)
    emit('acknowledge', {'message': f"Joined room for {USERNAME}"})
    print(f"{USERNAME} joined their room")

@user1_bp.socketio.on('leave_user_room')
def handle_leave_user_room():
    leave_room(USERNAME)
    emit('acknowledge', {'message': f"Left room for {USERNAME}"})
    print(f"{USERNAME} left their room")

@user1_bp.socketio.on('receive_message')
def handle_receive_message(data):
    sender = data.get('sender')
    message = data.get('message')
    emit('acknowledge', {'message': f"Message received from {sender}: {message}"})