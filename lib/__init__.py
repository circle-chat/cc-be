from flask import Flask
from config import Config
from flask_socketio import SocketIO
from flask_mongoengine import MongoEngine


app = Flask(__name__)
app.config.from_object(Config)
app.config['MONGODB_SETTINGS'] = {
  'host': 'mongodb://localhost/cc-be'
}
db = MongoEngine(app)
socketio = SocketIO(app, cors_allowed_origins="*")

from lib import routes, models
