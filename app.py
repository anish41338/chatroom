from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Secure this in production
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Dynamically register blueprints from the 'blueprints' folder
def register_blueprints(app):
    blueprint_dir = os.path.join(os.path.dirname(__file__), 'blueprints')
    for filename in os.listdir(blueprint_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = f"blueprints.{filename[:-3]}"  # Remove .py
            module = __import__(module_name, fromlist=['bp'])
            app.register_blueprint(module.bp)
            print(f"Registered blueprint: {module_name}")

# SocketIO event to handle global connection
@socketio.on('connect')
def handle_connect():
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"Client disconnected: {request.sid}")

if __name__ == '__main__':
    register_blueprints(app)
    socketio.run(app, host='localhost', port=5000, debug=True)