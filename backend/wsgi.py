"""Application entry point."""
from werkzeug.serving import run_simple

from my_dash import init_app


app = init_app()


if __name__ == '__main__':
    run_simple(hostname='127.0.0.1', port=8080, application=app)
