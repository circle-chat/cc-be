from lib import app, socketio, db
from lib.routes import add_group
from lib.models import Connection

def test_socketio_connection():
  flask_test_client = app.test_client()

  socketio_test_client = socketio.test_client(app, flask_test_client=flask_test_client)
  socketio_test_client2 = socketio.test_client(app, flask_test_client=flask_test_client)

  assert socketio_test_client.is_connected()

  assert socketio_test_client2.is_connected()


def test_client_can_connect_to_room():
  flask_test_client = app.test_client()
  socketio_test_client = socketio.test_client(app, flask_test_client=flask_test_client)
  socketio_test_client2 = socketio.test_client(app, flask_test_client=flask_test_client)

  socketio_test_client.emit('join_room', {'room': 'test'})

  welcome = socketio_test_client.get_received()

  message = welcome[0]['args']
  assert message == "Welcome to the test room"

  client2_data = socketio_test_client2.get_received()
  assert client2_data == []


def test_server_can_send_message_to_room():
  flask_test_client = app.test_client()
  socketio_test_client = socketio.test_client(app, flask_test_client=flask_test_client)
  socketio_test_client2 = socketio.test_client(app, flask_test_client=flask_test_client)
  socketio_test_client.emit('join_room', {'room': 'test'})
  client1_data = socketio_test_client.get_received()

  socketio_test_client.emit('message', {'message': 'Hello World', 'room': 'test'})

  client1_data = socketio_test_client.get_received()

  message = client1_data[0]['args']
  assert message == "Hello World"

  client2_data = socketio_test_client2.get_received()

  assert client2_data == []


def test_each_connected_client_in_room_sees_message():
  flask_test_client = app.test_client()
  socketio_test_client = socketio.test_client(app, flask_test_client=flask_test_client)
  socketio_test_client2 = socketio.test_client(app, flask_test_client=flask_test_client)
  socketio_test_client.emit('join_room', {'room': 'test'})
  socketio_test_client2.emit('join_room', {'room': 'test'})
  client1_data = socketio_test_client.get_received()
  client2_data = socketio_test_client2.get_received()

  socketio_test_client.emit('message', {'message': 'Hello World 2', 'room': 'test'})

  client1_data = socketio_test_client.get_received()

  client1_message = client1_data[0]['args']
  assert client1_message == "Hello World 2"

  client2_data = socketio_test_client2.get_received()
  client2_message = client2_data[0]['args']

  assert client2_message == "Hello World 2"


def test_each_connected_client_in_room_sees_when_leaving():
  flask_test_client = app.test_client()
  socketio_test_client = socketio.test_client(app, flask_test_client=flask_test_client)
  socketio_test_client2 = socketio.test_client(app, flask_test_client=flask_test_client)
  socketio_test_client.emit('join_room', {'room': 'test'})
  socketio_test_client2.emit('join_room', {'room': 'test'})
  socketio_test_client.get_received()
  client2_data = socketio_test_client2.get_received()

  socketio_test_client.emit('leave', {'room': 'test'})

  client2_data = socketio_test_client2.get_received()
  client2_message = client2_data[0]['args']

  assert client2_message == "A User left the test room"


def test_broadcast_message():
  flask_test_client = app.test_client()
  socketio_test_client = socketio.test_client(app, flask_test_client=flask_test_client)
  socketio_test_client2 = socketio.test_client(app, flask_test_client=flask_test_client)
  socketio_test_client.emit('join_room', {'room': 'test'})
  client1_data = socketio_test_client.get_received()
  client2_data = socketio_test_client2.get_received()

  socketio_test_client.emit('gmessage', 'Hello Everyone')

  client1_data = socketio_test_client.get_received()

  client1_message = client1_data[0]['args']
  assert client1_message == "Hello Everyone"

  client2_data = socketio_test_client2.get_received()
  client2_message = client2_data[0]['args']

  assert client2_message == "Hello Everyone"

# def test_can_add_a_group():
#   flask_test_client = app.test_client()
#   group_test =

def test_active_sockets():
  Connection.objects.delete()

  assert len(Connection.objects(group='test2')) == 0

  flask_test_client = app.test_client()
  socketio_test_client = socketio.test_client(app, flask_test_client=flask_test_client)
  socketio_test_client.emit('join_group', {'access_code': "test2"})
  conn1 = Connection.objects.get(sid=socketio_test_client.sid)

  assert len(Connection.objects(group='test2')) == 1
  assert conn1.sid == socketio_test_client.sid

  socketio_test_client2 = socketio.test_client(app, flask_test_client=flask_test_client)
  socketio_test_client2.emit('join_group', {'access_code': "test2"})
  conn2 = Connection.objects.get(sid=socketio_test_client2.sid)

  assert len(Connection.objects(group='test2')) == 2
  assert conn2.sid == socketio_test_client2.sid

  socketio_test_client.disconnect()

  assert len(Connection.objects(group='test2')) == 1

  socketio_test_client2.disconnect()

  assert len(Connection.objects(group='test2')) == 0

def test_group_connection_differentiation():
  Connection.objects.delete()

  assert len(Connection.objects(group='test')) == 0
  assert len(Connection.objects(group='test2')) == 0

  flask_test_client = app.test_client()
  socketio_test_client = socketio.test_client(app, flask_test_client=flask_test_client)
  socketio_test_client2 = socketio.test_client(app, flask_test_client=flask_test_client)
  socketio_test_client.emit('join_group', {'access_code': 'test'})
  socketio_test_client2.emit('join_group', {'access_code': 'test2'})

  assert len(Connection.objects(group='test')) == 1
  assert len(Connection.objects(group='test2')) == 1
  assert len(Connection.objects) == 2

  socketio_test_client2.disconnect()

  assert len(Connection.objects(group='test')) == 1
  assert len(Connection.objects(group='test2')) == 0
  assert len(Connection.objects) == 1


if __name__ == 'app':
  socketio_test()
