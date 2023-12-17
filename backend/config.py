"""Flask config."""
# from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Config:
    FLASK_APP = 'application.py'
    # SECRET_KEY = getenv('SECRET_KEY')
    SECRET_KEY = 'MY_TEMP_KEY'

    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    SQLALCHEMY_DATABASE_URI = 'sqlite:///project_db.db'
