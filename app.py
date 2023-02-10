from flask import request

from app_setup import (
    app,
)
from database import (
    database_create,
    database_drop,
    database_seed,
)
from endpoints import (
    parameters,
    url_parameters,
    planets,
    register,
    login,
    planet_details,
    add_planet,
    update_planet,
    delete_planet,
)


# Database operations
@app.cli.command('db_create')
def db_create():
    database_create()


@app.cli.command('db_drop')
def db_drop():
    database_drop()


@app.cli.command('db_seed')
def db_seed():
    database_seed()


# Endpoints routes
@app.route('/parameters')
def call_parameters():
    return parameters(request)


@app.route('/url_parameters/<string:name>/<int:age>')
def call_url_parameters(name: str, age: int):
    return url_parameters(name=name, age=age)


@app.route('/planets', methods=['GET'])
def call_planets():
    return planets()


@app.route('/register', methods=['POST'])
def call_register():
    return register(request)


@app.route('/login', methods=['POST'])
def call_login():
    return login(request)


@app.route('/planet_details/<int:planet_id>', methods=["GET"])
def call_planet_details(planet_id: int):
    return planet_details(planet_id)


@app.route('/add_planet', methods=['POST'])
def call_add_planet():
    return add_planet(request)


@app.route('/update_planet', methods=['PUT'])
def call_update_planet():
    return update_planet(request)


@app.route('/delete_planet/<int:planet_id>', methods=['DELETE'])
def call_delete_planet(planet_id: int):
    return delete_planet(planet_id)


if __name__ == '__main__':
    app.run()
