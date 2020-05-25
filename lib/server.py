from flask import Flask, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

app.config['SECRET_KEY'] = 'teamawesome'
app.debug = True
app.host = 'localhost'

# Recieve Message. Namespace is an example
@socketio.on('message', namespace='/group/test')
def recieve_message(message):
    print('received message: ' + message)

# Send Message. Namespace is an example
@socketio.on('message')
def send_message(message):
    send(message, namespace='/group/test')

# Join a room. `on_join` expects a dictionary argument.
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)

# Leave a room. `on_leave` expect a dictionary argument.
@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)

# Global Broadcast.
@socketio.on("message")
def handleMessage(msg):
  print(msg)
  send(msg, broadcast=True)
  return None

# Error handling default.
@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"]) # "my error event"
    print(request.event["args"])    # (data,)

if __name__ == '__main__':
    socketio.run(app)