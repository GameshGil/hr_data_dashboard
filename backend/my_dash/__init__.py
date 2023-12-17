"""Initialize Flask app."""
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from my_dash.dashboards import init_dashboard

migrate = Migrate()
csrf = CSRFProtect()
login_manager = LoginManager()


def create_app():
    """Construct core Flask app."""
    app = Flask(__name__, instance_relative_config=False)

    config_filename = 'config.Config'
    app.config.from_object(config_filename)

    from my_dash.models import db
    db.init_app(app)

    migrate.init_app(app=app, db=db)
    csrf.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from . import routes

        dash_app = init_dashboard()
        app.wsgi_app = DispatcherMiddleware(
            app.wsgi_app,
            {"/dashboards1": dash_app.server.wsgi_app},
        )
        return app
