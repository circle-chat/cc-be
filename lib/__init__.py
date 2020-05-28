from flask import Flask, request, Response
from flask_socketio import SocketIO, send, emit, join_room, leave_room, rooms
from flask_mongoengine import MongoEngine
# from database.mongodb import initialize_db
from database.models import Group


app = Flask(__name__)

from app import routes