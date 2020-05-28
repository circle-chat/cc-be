from flask import request, Response, url_for
from lib import app, db, socketio
from flask_socketio import send, emit, join_room, leave_room, rooms
from mongoengine import *
from lib.models import Group
from datetime import datetime
import secrets


# Test group room route
@app.route('/groups', methods=['POST'])
def add_group():
  body = request.form
  if body.name == '' and body.description == '':
    group = Group(
      name=body['name'],
      description=body['description'],
      access_code=secrets.token_hex(4),
      rules=body['rules'],
      created=datetime.utcnow
    ).save()
    return Response(group.to_json(), mimetype="application/json", status=200)
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
  Group.objects(access_code=access_code).get_or_404()

@app.route('/groups', methods=['GET'])
def get_groups():
  groups = Group.objects().to_json()
  return Response(groups, mimetype="application/json", status=200)
  
# # Join a group
# @socketio.on('join_group')
# def on_join_group(data):

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
  print(request.event["message"]) # "my error event"
  print(request.event["args"])    # (data,)

if __name__ == '__main__':
    socketio.run(app)
