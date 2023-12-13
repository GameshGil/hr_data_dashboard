"""Forms for main Flask app."""
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField
from wtforms import SelectField, SubmitField, FileField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
    """User registration form"""
    username = StringField('ФИО пользователя', validators=[DataRequired()])
    email = EmailField('Email пользователя', validators=[DataRequired()])
    role = SelectField(
        'Роль',
        choices=[
            ('user', 'Пользователь'),
            ('manager', 'Менеджер'),
            ('admin', 'Администратор')
        ],
        validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_repeat = PasswordField(
        'Введите пароль повторно', validators=[DataRequired()])
    submit = SubmitField('Подтвердить')


class LoginForm(FlaskForm):
    """User login form"""
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class DataForm(FlaskForm):
    """Data loading form"""
    load_data = FileField(
        'Выбрать обрабатываемые данные', validators=[DataRequired()])
    submit = SubmitField('Отправить')
