import os

from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')

# Makes server reload in real time
app.debug = True

db = SQLAlchemy(app)
marsh = Marshmallow(app)

@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('Database created.')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('Database dropped.')


@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(
        planet_name='Mercury',
        planet_type='Class D',
        home_star='Sol',
        mass=3.258e23,
        radius=1516,
        distance=35.98e6,
    )
    venus = Planet(
        planet_name='Venus',
        planet_type='Class K',
        home_star='Sol',
        mass=4.867e24,
        radius=3760,
        distance=67.24e6,
    )
    earth = Planet(
        planet_name='Earth',
        planet_type='Class M',
        home_star='Sol',
        mass=5.972e24,
        radius=3959,
        distance=92.96e6,
    )

    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = User(
        first_name='Vitor',
        last_name='Toledo',
        email='vitor@toledo.com',
        password='passowrd',
    )

    db.session.add(test_user)
    db.session.commit()
    print('Database seeded.')


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


@app.route('/planets', methods=['GET'])
def planets():
    planets_list = Planet.query.all()
    data = planets_schema.dump(planets_list)
    return jsonify(data=data)


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
    # mass in kg
    mass = Column(Float)
    #radius in miles
    radius = Column(Float)
    # miles distance from the star
    distance = Column(Float)


class UserSchema(marsh.Schema):
    class Meta:
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'password',
        )


class PlanetSchema(marsh.Schema):
    class Meta:
        fields = (
            'planet_id',
            'planet_name',
            'planet_type',
            'home_star',
            'mass',
            'radius',
            'distance',
        )


user_schema = UserSchema()
users_schema = UserSchema(many=True)

planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)


if __name__ == '__main__':
    app.run()
