from app.app import app, socketio, find_group

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

def test_user_can_only_join_group_if_access_code_right():
  flask_test_client = app.test_client()
  socketio_test_client = socketio.test_client(app, flask_test_client=flask_test_client)
  socketio_test_client2 = socketio.test_client(app, flask_test_client=flask_test_client)
  
  socketio_test_client.emit('join_group', {'access_code': "test2"})
  socketio_test_client2.emit('join_group', {'access_code': "test23334"})

  client1_data = socketio_test_client.get_received()
  client2_data = socketio_test_client.get_received()

  client1_message = client1_data[0]['args']
  assert client1_message == "Successfully Connected to Group"

  # client2_message = client2_data[0]['args']
  # assert client2_message == "Group Not Found"



def test_can_find_group_by_access_code():
  first_check = find_group('test2')
  second_check = find_group('sdfsdfsd')

  assert first_check == True
  assert second_check == False



if __name__ == 'app':
  socketio_test()