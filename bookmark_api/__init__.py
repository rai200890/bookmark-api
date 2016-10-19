from os import environ
from os.path import join, dirname

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_cache import Cache


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


db = SQLAlchemy(app)
api = Api(app)
CORS(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
