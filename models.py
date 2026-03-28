from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz 

IST = pytz.timezone('Asia/Kolkata')


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))


class BMI(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    bmi_value = db.Column(db.Float)
    user_id = db.Column(db.Integer)


class Water(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float)
    entry_date = db.Column(db.String(20))
    user_id = db.Column(db.Integer)


class BP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    systolic = db.Column(db.Integer)
    diastolic = db.Column(db.Integer)
    entry_date = db.Column(db.String(20))
    user_id = db.Column(db.Integer)


class Sugar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sugar_level = db.Column(db.Float)
    entry_date = db.Column(db.String(20))
    user_id = db.Column(db.Integer)


class Mood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mood = db.Column(db.String(50))
    note = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=lambda: datetime.now(IST))
    user_id = db.Column(db.Integer)