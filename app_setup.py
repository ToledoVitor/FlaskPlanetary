import os

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
app.config['JWT_SECRET_KEY'] = 'very-secret'
# Makes server reload in real time
app.debug = True

db = SQLAlchemy(app)

# Model serialization
marsh = Marshmallow(app)

# Authentication
jwt = JWTManager(app)
