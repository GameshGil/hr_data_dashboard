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

    # SQLALCHEMY_DATABASE_URI = 'sqlite:///project_db.db'

    POSTGRES_USER = 'Saeed'
    POSTGRES_PASSWORD = 'qwerty'
    POSTGRES_DB = 'flask'
    DB_HOST = 'flask-db'
    DB_PORT = '5432'
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
        f'@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}')
