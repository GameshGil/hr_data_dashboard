from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    username = StringField('ФИО пользователя', validators=[DataRequired()])
    email = EmailField('Email пользователя', validators=[DataRequired()])
    role = StringField('Роль', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_repeat = PasswordField(
        'Введите пароль повторно', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    username = StringField('ФИО пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Авторизироваться')
