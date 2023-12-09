import datetime as dt

from flask_login import UserMixin
from config import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.String(31), nullable=False)
    hashed_password = db.Column(db.String)
    registration_date = db.Column(db.DateTime, default=dt.datetime.now)
