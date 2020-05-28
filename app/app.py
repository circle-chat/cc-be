from database.mongodb import initialize_db
from database.models import Group, Connection
from flask import Flask, request, Response
from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Connect the app to the MongoDB
app.config['MONGODB_SETTINGS'] = {
  'host': 'mongodb://localhost/cc-be'
}

initialize_db(app)

def find_group(access_code):
  if Group.objects(access_code= f"{access_code}"):
    return True
  else:
    return False

# app.config['SECRET_KEY'] = 'teamawesome'
# app.debug = True
# app.host = 'localhost'

# Test group room route
@app.route('/groups', methods=['POST'])
def add_group():
  body = request.form
  group = Group(**body).save()
  return Response(group, mimetype="application/json", status=200)


# Send Message. Namespace is an example
@socketio.on('message')
def send_message(data):
  room = data['room']
  msg = data['message']
  # print(data['message'], room=room)
  send(msg, room=room)

# Join a group based on access_code
@socketio.on('join_group')
def group_join(data):
  if find_group(data['access_code']):
    room = data['access_code']
    try:
      Connection(group=room, sid=request.sid).save()
      join_room(room)
    except:
      print('something went wrong with adding the connection')
    send('Successfully Connected to Group', room=room)
  else:
    raise ConnectionRefusedError('Group Not Found')


# Remove connection from DB upon disconnect
@socketio.on('disconnect')
def on_disconnect():
    connection = Connection.objects.get_or_404(sid=request.sid)
    try:
      connection.delete()
    except:
      print('something went wrong with deleting the connection')

# Join a room. `on_join` expects a dictionary argument.
@socketio.on('join_room')
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
