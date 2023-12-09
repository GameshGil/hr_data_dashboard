from flask import render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user

from config import app, db
from models import User
from forms import RegistrationForm, LoginForm


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            email = form.email.data
            role = form.role.data
            password = form.password.data
            hashed_password = generate_password_hash(
                password=password,
                method='sha256'
            )
            new_user = User(
                username=username,
                email=email,
                role=role,
                hashed_password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first_or_404()

            if user and check_password_hash(user.hashed_password, password):
                login_user(user)
                return redirect(url_for('index'))

    return render_template('login.html', form=form)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=8080, debug=True)
