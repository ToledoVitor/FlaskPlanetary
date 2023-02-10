import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URL'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')

# Makes server reload in real time
app.debug = True

db = SQLAlchemy(app)


@app.route('/')
def hello_world():
    return jsonify(message='Hello World!'), 200


@app.route('/super_simple')
def super_simple():
    return jsonify(message='Hello from the Planetary API!'), 200


@app.route('/not_found')
def not_found():
    return jsonify(message='Resource not found'), 404


@app.route('/parameters')
def parameters():
    name = str(request.args.get('name'))
    age = int(request.args.get('age'))

    if age < 18:
        return jsonify(message=f'sorry, {name}, you are not old enough'), 403
    return jsonify(message=f'welcome {name}, you are old enough'), 200


@app.route('/url_parameters/<string:name>/<int:age>')
def url_parameters(name: str, age: int):
    if age < 18:
        return jsonify(message=f'sorry, {name}, you are not old enough'), 403
    return jsonify(message=f'welcome {name}, you are old enough'), 200


# database models
class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    password = Column(String)


class Planet(db.Model):
    __tablename__ = 'planets'

    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance = Column(Float)


if __name__ == '__main__':
    app.run()