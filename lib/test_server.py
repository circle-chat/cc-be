from lib import app, socketio, db
from lib.routes import add_group
from lib.models import Connection, Group
from datetime import datetime

def setup_module():
  Group(
      name="Test",
      description="Test",
      access_code="test",
      rules="test",
      created=datetime.utcnow
  ).save()

  Group(
      name="Test2",
      description="Test2",
      access_code="test2",
      rules="test2",
      created=datetime.utcnow
  ).save()

def teardown_function():
  Connection.drop_collection()

def teardown_module():
  Group.drop_collection()
  Connection.drop_collection()

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

  socketio_test_client.emit('leave', {'room': 'test', 'return_to': ''})

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


def test_matchmaking():
  flask_test_client = app.test_client()
  client1 = socketio.test_client(app, flask_test_client=flask_test_client)
  client2 = socketio.test_client(app, flask_test_client=flask_test_client)
  client3 = socketio.test_client(app, flask_test_client=flask_test_client)
  room2 = f"room_{client2.sid}"

  client1.emit('join_group', {'access_code': 'test', 'name': 'Client 1'})
  data1 = client1.get_received()

  assert data1[0]['args'][0]['access_code'] == 'test'

  client2.emit('join_group', {'access_code': 'test', 'name': 'Client 2'})
  data1 = client1.get_received()
  data2 = client2.get_received()

  assert data1[0]['args'][0]['room'] == room2
  assert data2[1]['args'][0]['room'] == room2
  assert data1[-1]['args'] == "Client 2 connected."
  assert data2[-1]['args'] == "Client 2 connected."

  client3.emit('join_group', {'access_code': 'test'})
  data3 = client3.get_received()

  assert data3[0]['args'][0]['access_code'] == 'test'

  client1.emit('message', {'message': 'Client 3 should not see this', 'room': room2})
  data1 = client1.get_received()
  data2 = client2.get_received()
  data3 = client3.get_received()

  assert data1[-1]['args'] == 'Client 3 should not see this'
  assert data2[-1]['args'] == 'Client 3 should not see this'
  assert data3 == []


def test_leaving_sends_client_back_to_group():
  flask_test_client = app.test_client()
  client1 = socketio.test_client(app, flask_test_client=flask_test_client)
  client2 = socketio.test_client(app, flask_test_client=flask_test_client)
  room2 = f"room_{client2.sid}"

  client1.emit('join_group', {'access_code': 'test'})

  assert len(Group.objects(access_code='test')) == 1

  client2.emit('message', {'message': 'Test 1', 'room': 'test'})
  data1 = client1.get_received()

  assert data1[-1]['args'] == 'Test 1'

  client2.emit('join_group', {'access_code': 'test'})
  client2.emit('message', {'message': 'Test 2', 'room': 'test'})

  data1 = client1.get_received()

  assert data1[-1]['args'] != 'Test 2'

  client1.emit('leave', {'room': room2, 'return_to': 'test'})
  client2.emit('message', {'message': 'Test 3', 'room': 'test'})
  data1 = client1.get_received()

  assert data1[-1]['args'] == 'Test 3'


def test_automatic_matchmaking_after_leaving_room():
  flask_test_client = app.test_client()
  client1 = socketio.test_client(app, flask_test_client=flask_test_client)
  client2 = socketio.test_client(app, flask_test_client=flask_test_client)
  client3 = socketio.test_client(app, flask_test_client=flask_test_client)
  room1 = f"room_{client1.sid}"
  room2 = f"room_{client2.sid}"

  client1.emit('join_group', {'access_code': 'test'})
  client2.emit('join_group', {'access_code': 'test'})
  client3.emit('join_group', {'access_code': 'test'})

  client1.emit('leave', {'room': room2, 'return_to': 'test'})

  client3.emit('message', {'message': 'Clients 1 and 3 rule!', 'room': room1})
  data1 = client1.get_received()
  data2 = client2.get_received()
  data3 = client3.get_received()

  assert data1[-1]['args'] == 'Clients 1 and 3 rule!'
  assert data2[-1]['args'] != 'Clients 1 and 3 rule!'
  assert data3[-1]['args'] == 'Clients 1 and 3 rule!'


def test_name_sending():
  flask_test_client = app.test_client()
  client1 = socketio.test_client(app, flask_test_client=flask_test_client)
  client2 = socketio.test_client(app, flask_test_client=flask_test_client)
  room2 = f"room_{client2.sid}"

  client1.emit('join_group', {'access_code': 'test', 'name': 'Client 1'})
  client2.emit('join_group', {'access_code': 'test', 'name': 'Client 2'})
  data1 = client1.get_received()
  data2 = client2.get_received()

  assert data1[1]['args'][0]['match'] == 'Client 2'
  assert data2[1]['args'][0]['match'] == 'Client 1'