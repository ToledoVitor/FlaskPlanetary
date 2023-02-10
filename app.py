import os

from flask import Flask, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    JWTManager,
    jwt_required,
)
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
app.config['JWT_SECRET_KEY'] = 'very-secret'

# Makes server reload in real time
app.debug = True

db = SQLAlchemy(app)
marsh = Marshmallow(app)
jwt = JWTManager(app)

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
    mercury = Planet(planet_name='Mercury',
                     planet_type='Class D',
                     home_star='Sol',
                     mass=3.258e23,
                     radius=1516,
                     distance=35.98e6)

    venus = Planet(planet_name='Venus',
                   planet_type='Class K',
                   home_star='Sol',
                   mass=4.867e24,
                   radius=3760,
                   distance=67.24e6)

    earth = Planet(planet_name='Earth',
                   planet_type='Class M',
                   home_star='Sol',
                   mass=5.972e24,
                   radius=3959,
                   distance=92.96e6)

    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = User(first_name='Vitor',
                     last_name='Toledo',
                     email='vitor@toledo.com',
                     password='passowrd')

    db.session.add(test_user)
    db.session.commit()
    print('Database seeded.')


@app.route('/parameters')
def parameters():
    name = str(request.args.get('name'))
    age = int(request.args.get('age'))

    if age < 18:
        return jsonify(message=f'sorry, {name}, you are not old enough.'), 403
    return jsonify(message=f'welcome {name}, you are old enough.'), 200


@app.route('/url_parameters/<string:name>/<int:age>')
def url_parameters(name: str, age: int):
    if age < 18:
        return jsonify(message=f'sorry, {name}, you are not old enough.'), 403
    return jsonify(message=f'welcome {name}, you are old enough.'), 200


@app.route('/planets', methods=['GET'])
def planets():
    planets_list = Planet.query.all()
    data = planets_schema.dump(planets_list)
    return jsonify(data=data)


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    email_exists = User.query.filter_by(email=email).first()

    if email_exists:
        return jsonify(message='Email already exists.'), 409

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    password = request.form['password']

    user = User(first_name=first_name, last_name=last_name, email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify(messsage='User created successfully.'), 201


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    user = User.query.filter_by(email=email, password=password).first()
    if user:
        access_token = create_access_token(identity=email)
        return jsonify(message='Login succeeded!', access_token=access_token), 200
    else:
        return jsonify(message='Bad email or password.'), 401 


@app.route('/planet_details/<int:planet_id>', methods=["GET"])
def planet_details(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if not planet:
        return jsonify(message="That planet does not exist."), 404
    
    data = planet_schema.dump(planet)
    return jsonify(data)


@app.route('/add_planet', methods=['POST'])
def add_planet():
    planet_name = request.form['planet_name']
    planet_exists = Planet.query.filter_by(planet_name=planet_name).first()

    if planet_exists:
        return jsonify(message='That planet already exists.'), 409
    
    planet_type = request.form['planet_type']
    home_star = request.form['home_star']
    mass = float(request.form['mass'])
    radius = float(request.form['radius'])
    distance = float(request.form['distance'])

    new_planet = Planet(planet_name=planet_name,
                        planet_type=planet_type,
                        home_star=home_star,
                        mass=mass,
                        radius=radius,
                        distance=distance)

    db.session.add(new_planet)
    db.session.commit()
    return jsonify(message='You added the planet.'), 201


@app.route('/update_planet', methods=['DELETE'])
def update_planet():
    planet_id = int(request.form['planet_id'])
    planet = Planet.query.filter_by(planet_id=planet_id).first()

    if not planet:
        return jsonify(message='That planet does not exists.'), 404

    planet.planet_name = request.form['planet_name']
    planet.planet_type = request.form['planet_type']
    planet.home_star = request.form['home_star']
    planet.mass = float(request.form['mass'])
    planet.radius = float(request.form['radius'])
    planet.distance = float(request.form['distance'])
    db.session.commit()
    return jsonify(message='You updated the planet.'), 202


@app.route('/delete_planet/<int:planet_id>', methods=['PUT'])
def delete_planet(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()

    if not planet:
        return jsonify(message='That planet does not exists.'), 404

    db.session.delete(planet)
    return jsonify(message='You deleted the planet.'), 202

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
