"""Routes for main Flask app."""
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, redirect, url_for
from flask import current_app as app
from flask_login import login_user, logout_user, login_required, current_user

from my_dash.models import User
from my_dash.forms import RegistrationForm, LoginForm, DataForm
from my_dash.commands import load_csv_from_folder, add_csv_to_db


from my_dash import db


@app.login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route("/")
def index():
    """Index page for Flask app."""
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page."""
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        role = form.role.data
        password = form.password.data
        password_repeat = form.password_repeat.data
        if password != password_repeat:
            return render_template(
                'register.html',
                form=form,
                message='Ошибка при вводе пароля'
            )
        if User.query.filter(User.email == email).first():
            return render_template(
                'register.html',
                form=form,
                message='Пользователь уже зарегистрирован'
            )
        hashed_password = generate_password_hash(password)
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
    """User login page."""
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember = form.remember_me.data
        user = User.query.filter_by(email=email).first_or_404()

        if user and check_password_hash(user.hashed_password, password):
            login_user(user, remember=remember)
            return redirect(url_for('index'))
        return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    """User logout page."""
    logout_user()
    return redirect(url_for('login'))


@app.route('/load_data', methods=['GET', 'POST'])
@login_required
def loading_data():
    """Loading data for analytics page."""
    form = DataForm()
    is_load_data = False
    wrong_data_type = False
    if form.validate_on_submit():
        load_data = form.load_data.data
        if load_data.filename.split('.')[-1] == 'csv':
            is_load_data = True
            add_csv_to_db(load_data)
        else:
            wrong_data_type = True
    return render_template(
            'load_data.html',
            form=form,
            is_load=is_load_data,
            wrong_data_type=wrong_data_type)


@app.route('/load_data_from_file', methods=['POST'])
@login_required
def load_data_from_file():
    """Route for loading data from file."""
    print(current_user.role)
    if current_user.role == 'user':
        load_csv_from_folder()
        return redirect('/dashboards1')
    return redirect('/load_data')


# @app.route('/dashboards1', methods=['GET', 'POST'])
# @login_required
# def dashboards1():
#     return render_template('dashboards1.html')


@app.errorhandler(401)
def not_authorized(error):
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(405)
def wrong_method(error):
    return render_template('405.html'), 405


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500
