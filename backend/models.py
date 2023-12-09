from config import db


class User(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    role = db.Column(db.Text, nullable=False)
