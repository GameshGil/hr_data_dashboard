"""Application entry point."""
from werkzeug.serving import run_simple

from my_dash import create_app


app = create_app('config.Config')


if __name__ == '__main__':
    run_simple(hostname='127.0.0.1', port=8080, application=app)
