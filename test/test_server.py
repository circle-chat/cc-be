from lib.server import app, socketio

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

  socketio_test_client.emit('join', {'room': 'test'})

  welcome = socketio_test_client.get_received()

  message = welcome[0]['args']
  assert message == "Welcome to the test room"

  client2_data = socketio_test_client2.get_received()
  assert client2_data == []


def test_server_can_send_message_to_room():
  flask_test_client = app.test_client()
  socketio_test_client = socketio.test_client(app, flask_test_client=flask_test_client)
  socketio_test_client2 = socketio.test_client(app, flask_test_client=flask_test_client)
  socketio_test_client.emit('join', {'room': 'test'})
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
  socketio_test_client.emit('join', {'room': 'test'})
  socketio_test_client2.emit('join', {'room': 'test'})
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
  socketio_test_client.emit('join', {'room': 'test'})
  socketio_test_client2.emit('join', {'room': 'test'})
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
  socketio_test_client.emit('join', {'room': 'test'})
  client1_data = socketio_test_client.get_received()
  client2_data = socketio_test_client2.get_received()

  socketio_test_client.emit('gmessage', 'Hello Everyone')

  client1_data = socketio_test_client.get_received()

  client1_message = client1_data[0]['args']
  assert client1_message == "Hello Everyone"

  client2_data = socketio_test_client2.get_received()
  client2_message = client2_data[0]['args']

  assert client2_message == "Hello Everyone"



if __name__ == 'app':
  socketio_test()