from werkzeug.middleware.dispatcher import DispatcherMiddleware

from config import app, login_manager, dash_app
from models import User


@login_manager.user_loader
def load_user(user_id):
    return User.query.get_or_404(user_id)


from routes import *


application = DispatcherMiddleware(
    app,
    {"/dashboards1": dash_app.server},
)
