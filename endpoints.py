from flask import jsonify
from flask_jwt_extended import (
    create_access_token,
)

from app_setup import db
from database import (
    Planet,
    planet_schema,
    planets_schema,
    User,
)


def register(request):
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


def login(request):
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


def parameters(request):
    name = str(request.args.get('name'))
    age = int(request.args.get('age'))

    if age < 18:
        return jsonify(message=f'sorry, {name}, you are not old enough.'), 403
    return jsonify(message=f'welcome {name}, you are old enough.'), 200


def url_parameters(name: str, age: int):
    if age < 18:
        return jsonify(message=f'sorry, {name}, you are not old enough.'), 403
    return jsonify(message=f'welcome {name}, you are old enough.'), 200


def planets():
    planets_list = Planet.query.all()
    data = planets_schema.dump(planets_list)
    return jsonify(data=data)


def planet_details(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()
    if not planet:
        return jsonify(message="That planet does not exist."), 404
    
    data = planet_schema.dump(planet)
    return jsonify(data)


def add_planet(request):
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


def update_planet(request):
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


def delete_planet(planet_id: int):
    planet = Planet.query.filter_by(planet_id=planet_id).first()

    if not planet:
        return jsonify(message='That planet does not exists.'), 404

    db.session.delete(planet)
    return jsonify(message='You deleted the planet.'), 202
