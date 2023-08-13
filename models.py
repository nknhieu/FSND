import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(app, db)

class Vehicle(db.Model):
    __tablename__ = 'Vehicle'
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(120))
    model = db.Column(db.String(120))
    year = db.Column(db.String(120))
    color = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    rentalprice = db.Column(db.Integer)
    rentals = db.relationship('Rental', backref='vehicle', lazy=True)

class Customer(db.Model):
    __tablename__ = 'Customer'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120))
    lastname = db.Column(db.String(120))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    address = db.Column(db.String(120))
    rentals = db.relationship('Rental', backref='customer', lazy=True)

class Rental(db.Model):
    __tablename__ = 'Rental'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer,db.ForeignKey('Vehicle.id')
                          ,nullable=False)
    customer_id = db.Column(db.Integer,db.ForeignKey('Customer.id')
                          ,nullable=False)
    rentaldate = db.Column(db.DateTime, nullable=False)
    returndate = db.Column(db.DateTime, nullable=False)
    totalcost = db.Column(db.Integer)
    