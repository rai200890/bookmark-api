from os import environ
from os.path import join, dirname

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api


dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def parse_boolean(value):
    return value in ['True', 'true']


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = parse_boolean(environ.get('SQLALCHEMY_TRACK_MODIFICATIONS'))

db = SQLAlchemy(app)

api = Api(app)
