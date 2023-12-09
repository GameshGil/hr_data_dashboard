from flask import render_template

from config import app, db, migrate, csrf
from models import User
from forms import UserForm


@app.route("/")
def index():
    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=8080, debug=True)
