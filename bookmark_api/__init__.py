from os import environ
from os.path import join, dirname

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_caching import Cache


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def parse_boolean(value):
    return value in ['True', 'true']


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = parse_boolean(environ.get('SQLALCHEMY_TRACK_MODIFICATIONS'))
app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
app.config['JWT_VERIFY'] = parse_boolean(environ.get('JWS_VERIFY'))
app.config['JWT_AUTH_HEADER_PREFIX'] = "Bearer"
app.config['CORS_ORIGINS'] = environ.get('CORS_ORIGINS')
app.config['CACHE_TYPE'] = environ.get('CACHE_TYPE')
app.config['CACHE_REDIS_URL'] = environ.get('CACHE_REDIS_URL')
app.config['CACHE_DEFAULT_TIMEOUT'] = environ.get('CACHE_DEFAULT_TIMEOUT')
app.config['CACHE_NO_NULL_WARNING'] = environ.get('CACHE_NO_NULL_WARNING')
app.config['CACHE_KEY_PREFIX'] = environ.get('CACHE_KEY_PREFIX')

db = SQLAlchemy(app)
api = Api(app)
CORS(app)
cache = Cache(app)
