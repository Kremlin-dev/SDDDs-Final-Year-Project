from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    company_name = db.Column(db.String(120), nullable=True)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.String(50), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    time_moved = db.Column(db.DateTime, nullable=False)
    drowsiness_state = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(120), nullable=True)
    car_type = db.Column(db.String(120), nullable=True)
    driver = db.Column(db.String(120), nullable=True)
    reg_year = db.Column(db.String(120), nullable=True)
