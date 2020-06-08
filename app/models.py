from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class FlightPlan(db.Model):
    __tablename__ = 'flight_plans'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    route = db.Column(db.ARRAY(db.Integer))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", back_populates="flightPlans")


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    nickname = db.Column(db.String)
    name = db.Column(db.String)

    flightPlans = db.relationship("FlightPlan", back_populates='user')
    airplanes = db.relationship("Airplane", back_populates='user')


class AirPlane(db.Model):
    __tablename__ = 'airplanes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    fuel_load = db.Column(db.Float)
    flow_rate = db.Column(db.Float)
    net_thrust = db.Column(db.Float)
    fuel_comsumption = db.Column(db.Float)
    speed = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", back_populates="airplanes")


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
    atc_tower = db.Column(db.Boolean)
    ctaf = db.Column(db.Float)
    landing_fee = db.Column(db.Boolean)