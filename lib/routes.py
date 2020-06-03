from flask import request, Response, url_for
from circle import app, db, socketio
from flask_socketio import send, emit, join_room, leave_room, rooms
from lib.models import Group, Connection
from datetime import datetime
import secrets


# Test group room route
@app.route('/groups', methods=['POST'])
def add_group():
  body = request.json
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
    return Response('Please enter a group name and description.', status=400)

# Send Message. Namespace is an example
@socketio.on('message')
def send_message(data):
  room = data['room']
  msg = data['message']
  # print(data['message'], room=room)
  emit('message', data, room=room)

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
    group = data['access_code']
    room = None
    name = 'Anonymous'
    if 'name' in data.keys():
      name = data['name']
    try:
      Connection(group=group, sid=request.sid, created=datetime.utcnow, user_name=name).save()
      join_room(group)
      # emit('join_group', {'sid': user.sid, 'name': user.user_name, 'access_code': group}, room=user.sid)
      matchmake(group)
    except:
      print('Unable to create connection')
  else:
    raise ConnectionRefusedError('Group Not Found')

def matchmake(group):
  match = None
  my_conn = Connection.objects(sid=request.sid).first()
  if len(Connection.objects(group=group, waiting=True)) > 1:
    for conn in Connection.objects(group=group, waiting=True):
      if conn.sid != request.sid and conn.sid != my_conn.last_match and conn.last_match != my_conn.sid:
        match = conn.sid

  if match:
    room = f"room_{request.sid}"
    join_room(room)
    join_room(sid=match, room=room)
    leave_room(room=group)
    leave_room(sid=match, room=group)
    their_conn = Connection.objects(sid=match).first()
    my_conn.waiting = False
    my_conn.last_match = their_conn.sid
    my_conn.save()
    their_conn.waiting = False
    their_conn.last_match = my_conn.sid
    their_conn.save()
    emit('join_room', {'room': room, 'user': my_conn.user_name, 'match': {'name':their_conn.user_name, 'sid':their_conn.sid}}, room=my_conn.sid)
    emit('join_room', {'room': room, 'user': their_conn.user_name, 'match': {'name':my_conn.user_name, 'sid':my_conn.sid}}, room=their_conn.sid)
    send(f'{my_conn.user_name} connected.', room=room)
    return room


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


# Leave a room. `on_leave` expect a dictionary argument.
@socketio.on('leave')
def on_leave(data):
  room = data['room']
  return_group = data['return_to']
  leave_room(room)
  send(f'A User left the {room} room', room=room)
  if return_group:
    my_conn = Connection.objects(sid=request.sid).first()
    my_conn.waiting = True
    my_conn.save()
    join_room(return_group)
    matchmake(return_group)


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
    socketio.run(app, host='0.0.0.0', port=8080)
