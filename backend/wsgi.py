from werkzeug.serving import run_simple
from app import application

if __name__ == '__main__':
    run_simple(hostname='127.0.0.1', port=8080, application=application)
