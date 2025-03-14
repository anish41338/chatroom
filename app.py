from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
import importlib

from user1 import bp as user1_bp, register_socketio_handlers as register_user1_handlers
from user2 import bp as user2_bp, register_socketio_handlers as register_user2_handlers
from user3 import bp as user3_bp, register_socketio_handlers as register_user3_handlers

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

app.register_blueprint(user1_bp)
app.register_blueprint(user2_bp)
app.register_blueprint(user3_bp)

register_user1_handlers(socketio)
register_user2_handlers(socketio)
register_user3_handlers(socketio)

@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")

if __name__ == '__main__':
    socketio.run(app, host='localhost', port=5000, debug=True)