import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project_db.db'

db = SQLAlchemy(app=app)
migrate = Migrate(app=app, db=db)

app.config['SECRET_KEY'] = SECRET_KEY
csrf = CSRFProtect(app)
