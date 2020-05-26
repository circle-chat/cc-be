from flask import Flask, request, Response
from database.mongodb import initialize_db
from database.models import Group
from flask_socketio import SocketIO, emit, send, join_room, leave_room
from flask_restx import Api, Resource, fields


# Create the application object of the Flask class
# __name__ name of the module (so in this case app - I think)
app = Flask(__name__)

# Connect the app to the MongoDB
app.config['MONGODB_SETTINGS'] = {
  'host': 'mongodb://localhost/cc-be'
}

initialize_db(app)

# def handleMessage(msg):
#   print(msg)
#   send(msg, broadcast=True)
#   return None

# Setup the Socket and allow CORS
socketIo = SocketIO(app, cors_allowed_origins="*")

# Create the API object from the Flask App, the version, Title and description)
api = Api(app, version='1.0', title='Circle Chat API', description='API for simple chat rooms')

# Create the namespace for the main resource of groups
ns = api.namespace('groups', description='Groups for chats')



# Test group room route
@app.route('/groups', methods=['POST'])
def add_group():
  body = request.form
  group = Group(**body).save()
  return Response(group, mimetype="application/json", status=200)

  # return { 'Group created.  Group Key:' key }, 200

# @app.route('/groups', methods=['GET'])
# def get_groups():
#   groups = Group.objects().to_json()
#   return Response(groups, mimetype="application/json", status=200)

@app.route('/groups/<access_code>', methods=['GET'])
def get_group(access_code):
  group = Group.objects.get(access_code=access_code)
  return group.access_code

# @socketIo.on('join')
# def on_join(data):
#   room = data['room']
#   join_room(room)
#   send("Welcome to the room", room=room)

# @socketIo.on('message')
# def handleMessage(msg):
#   print(msg)
#   send(msg, namespace=f'/groups/{access_code}')
#   return None





if __name__ == '__main__':
    socketIo.run(app)
  # return Response(group, mimetype="application/json", status=200)


# Create the 

print("test")

app.run()
