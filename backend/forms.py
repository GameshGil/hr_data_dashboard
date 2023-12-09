from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UserForm(FlaskForm):
    username = StringField('ФИО пользователя', validators=[DataRequired()])
    role = StringField('Роль', validators=[DataRequired()])
    submit = SubmitField('Добавить')
