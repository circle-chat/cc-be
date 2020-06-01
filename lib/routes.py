from flask import request, Response, url_for
from circle import app, db, socketio
from flask_socketio import send, emit, join_room, leave_room, rooms
from lib.models import Group, Connection
from datetime import datetime
import secrets


# Test group room route
@app.route('/groups', methods=['POST'])
def add_group():
  body = request.form
  if body['name'] != '' and body['description'] != '':
    try:
      group = Group(
        name=body['name'],
        description=body['description'],
        access_code=secrets.token_hex(4),
        rules=body['rules'],
        created=datetime.utcnow
      ).save()
      return Response(group.to_json(), mimetype="application/json", status=200)
    except:
      print('Group was not able to be created.')
  else:
    return Response('Please enter a group name and description.')

# Send Message. Namespace is an example
@socketio.on('message')
def send_message(data):
  room = data['room']
  msg = data['message']
  # print(data['message'], room=room)
  send(msg, room=room)

# Find a group
def find_group(access_code):
  if Group.objects(access_code=f"{access_code}"):
    return True
  else:
    return False

@app.route('/groups', methods=['GET'])
def get_groups():
  groups = Group.objects().to_json()
  return Response(groups, mimetype="application/json", status=200)

# # Join a group
@socketio.on('join_group')
def group_join(data):
  if find_group(data['access_code']):
    room = data['access_code']
    try:
      Connection(group=room, sid=request.sid, created=datetime.utcnow).save()
      join_room(room)
    except:
      print('something went wrong with adding the connection')
    send('Successfully Connected to Group', room=room)
  else:
    raise ConnectionRefusedError('Group Not Found')

# Remove connection from DB upon disconnect
@socketio.on('disconnect')
def on_disconnect():
    try:
      connection = Connection.objects.get(sid=request.sid)
      connection.delete()
    except:
      print('something went wrong with deleting the connection')

# Join a room. `on_join` expects a dictionary argument.
@socketio.on('join_room')
def on_join_room(data):
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
  print(request.event["message"])
  print(request.event["args"])

if __name__ == '__main__':
    socketio.run(app)
