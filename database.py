from sqlalchemy import Column, Integer, String, Float

from app_setup import db, marsh


def database_create():
    db.create_all()
    print('Database created.')


def database_drop():
    db.drop_all()
    print('Database dropped.')


def database_seed():
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

# Schemas to serialize the queryset to JSON
planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)
