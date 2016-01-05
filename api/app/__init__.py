__author__ = 'Serban Carlogea'

from flask import Flask
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

db = MongoEngine(app)

from app import api
