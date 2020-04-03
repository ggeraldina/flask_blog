""" This file contain all forms """
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    """ Class for a post form """
    title = StringField(label="Название:",
                        validators=[DataRequired(), Length(max=200)],
                        id="id_title")
    text = TextAreaField(label="Текст:", validators=[DataRequired()], id="id_text")

class LoginForm(FlaskForm):
    """ Class for a login form """
    username = StringField(label="Имя пользователя:", validators=[DataRequired()])
    password = PasswordField(label="Пароль:", validators=[DataRequired()])
    remember_me = BooleanField(label="Запомнить меня")
