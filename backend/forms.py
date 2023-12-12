from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, BooleanField
from wtforms import SelectField, SubmitField, FileField
from wtforms.validators import DataRequired


class RegistrationForm(FlaskForm):
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
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')


class DataForm(FlaskForm):
    load_data = FileField(
        'Выбрать обрабатываемые данные', validators=[DataRequired()])
    submit = SubmitField('Отправить')
