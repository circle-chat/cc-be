from flask import Flask
from config import Config
from flask_socketio import SocketIO
from flask_mongoengine import MongoEngine
from os import environ
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_object(['FLASK_ENV'])
db = MongoEngine(app)
socketio = SocketIO(app, cors_allowed_origins="*")

from lib import routes, models

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=int(environ.get('PORT', 8080)))
