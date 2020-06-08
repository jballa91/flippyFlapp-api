from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class FlightPlan(db.Model):
    __tablename__ = 'flight_plans'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    start_date = db.Column(db.DateTime(timezone=False))
    end_date = db.Column(db.DateTime(timezone=False))
    route = db.Column(db.ARRAY(db.Integer))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", back_populates="flightPlans")

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'route': self.route,
            'user_id': self.user_id,
            'user': self.user.toDict()
        }



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    nickname = db.Column(db.String)
    name = db.Column(db.String)

    flightPlans = db.relationship("FlightPlan", back_populates='user')
    airplanes = db.relationship("Airplane", back_populates='user')

    def toDict(self):
        return {
            'id': self.id,
            'email': self.email,
            'nickname': self.nickname,
            'name': self.name
        }

    def toDict(self):
        return {
            'id': self.id,
            'email': self.email,
            'nickname': self.nickname,
            'name': self.name,
            'flightPlans': self.flightPlans.toDict(),
            'airplanes': self.airplanes.toDict()
        }


class Airplane(db.Model):
    __tablename__ = 'airplanes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    fuel_load = db.Column(db.Float)
    fuel_consumption = db.Column(db.Float)
    speed = db.Column(db.Float)
    start_taxi_takeoff_fuel_use = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", back_populates="airplanes")

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'fuel_load': self.fuel_load,
            'fuel_consumption': self.fuel_consumption,
            'speed': self.speed,
            'start_taxi_takeoff_fuel_use': self.start_taxi_takeoff_fuel_use,
            'user_id': self.user_id
        }


class AirPort(db.Model):
    __tablename__ = 'airports'

    id = db.Column(db.Integer, primary_key=True)
    x_coord = db.Column(db.Float, nullable=False)
    y_coord = db.Column(db.Float, nullable=False)
    name = db.Column(db.String(100))
    city = db.Column(db.String(100))
    state = db.Column(db.String(5))
    loc_id = db.Column(db.String(10))
    manager_name = db.Column(db.String(100))
    manager_phone_number = db.Column(db.String(20))
    fss_phone_number = db.Column(db.String(20))
    sectional_chart = db.Column(db.String(50))
    elevation = db.Column(db.Integer)
    pattern_altitude = db.Column(db.Float)
    fuel_types = db.Column(db.String)
    atc_tower = db.Column(db.Boolean)
    ctaf = db.Column(db.Float)
    landing_fee = db.Column(db.Boolean)

    def toDict(self):
        return {
            "id": self.id,
            "x_coord": self.x_coord,
            "y_coord": self.y_coord,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'loc_id': self.loc_id,
            'manager_name': self.manager_name,
            'manager_phone_number': self.manager_phone_number,
            'fss_phone_number': self.fss_phone_number,
            'sectional_chart': self.sectional_chart,
            'elevation': self.elevation,
            'atc_tower': self.atc_tower,
            'ctaf': self.ctaf,
            'landing_fee': self.landing_fee
        }
