from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config(object):
  SECRET_KEY = environ.get('SECRET_KEY')


class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    MONGODB_HOST = environ.get('MONGO_HOST')
    MONGODB_DB = 'circle-chat'


class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
    MONGODB_HOST = environ.get('TEST_DATABASE_URL')
    
class TestConfig(Config):
    FLASK_ENV = 'testing'
    DEBUG = True
    TESTING = True
    MONGODB_HOST = environ.get('TEST_DATABASE_URL')
