from flask import render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import login_user

from config import app, db
from models import User
from forms import RegistrationForm, LoginForm, DataForm


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
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
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first_or_404()

        if user and check_password_hash(user.hashed_password, password):
            # login_user(user)
            return redirect(url_for('index'))

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    return redirect(url_for('login'))



@app.route('/load_data', methods=['GET', 'POST'])
def loading_data():
    form = DataForm()
    is_load_data = False
    print(is_load_data)
    if form.validate_on_submit():
        load_data = form.load_data.data
        is_load_data = True
        print(load_data)
    print(is_load_data)
    return render_template(
        'load_data.html', form=form, is_load=is_load_data)


@app.route('/dashboards1', methods=['GET', 'POST'])
def dashboards1():
    return render_template('dashboards1.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='127.0.0.1', port=8080, debug=True)
