from flask import Flask, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

app.config['SECRET_KEY'] = 'teamawesome'
app.debug = True
app.host = 'localhost'


# Send Message. Namespace is an example
@socketio.on('message')
def send_message(data):
  room = data['room']
  msg = data['message']
  # print(data['message'], room=room)
  send(msg, room=room)
  

# Join a room. `on_join` expects a dictionary argument.
@socketio.on('join')
def on_join(data):
  room = data['room']
  join_room(room)
  send(f'Welcome to the {room} room', room=room)
  # timer.limit = close_room()


# Leave a room. `on_leave` expect a dictionary argument.
@socketio.on('leave')
def on_leave(data):
  room = data['room']
  leave_room(room)
  send(f'A User left the {room} room', room=room)


# Global Broadcast.
@socketio.on("gmessage")
def handleMessage(msg):
  send(msg, broadcast=True)

# Error handling default.
@socketio.on_error_default
def default_error_handler(e):
  print(request.event["message"]) # "my error event"
  print(request.event["args"])    # (data,)

if __name__ == '__main__':
    socketio.run(app)