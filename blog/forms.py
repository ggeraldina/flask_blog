""" This file contain all forms """
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo

from . import MONGO


class PostForm(FlaskForm):
    """ Class for a post form """
    title = StringField(label="Название:",
                        validators=[DataRequired(message="Поле с названием должно быть заполнено."), 
                                    Length(max=200, message="Максимум 200 символов.")])
    text = TextAreaField(label="Текст:", 
                         validators=[DataRequired(message="Поле с текстом должно быть заполнено.")])

class LoginForm(FlaskForm):
    """ Class for a login form """
    username = StringField(label="Имя пользователя:", 
                           validators=[DataRequired(message="Введите имя пользователя."), 
                                       Length(max=30, message="Максимум 30 символов.")])
    password = PasswordField(label="Пароль:", 
                             validators=[DataRequired(message="Введите пароль.")])

    def validate_username(self, username):
        user = MONGO.db.blog_user.find_one({"username": username.data})
        if user is None:
            raise ValidationError("Пользователь с таким именем не существует. \
                                   Пожалуйста, попробуйте еще раз.")

class RegistrationForm(FlaskForm):
    username = StringField(label="Имя пользователя:", 
                           validators=[DataRequired(message="Введите имя пользователя."), 
                                       Length(max=30, message="Максимум 30 символов.")])
    password = PasswordField(label="Пароль:", 
                             validators=[DataRequired(message="Введите пароль.")])
    password2 = PasswordField(label="Повторите пароль:", 
                              validators=[DataRequired(message="Повторите пароль."), 
                                          EqualTo(fieldname="password", 
                                                  message="Пароль повторно введен неверно.")])

    def validate_username(self, username):
        user = MONGO.db.blog_user.find_one({"username": username.data})
        if user is not None:
            raise ValidationError("Пользователь с таким именем уже существует. \
                                   Пожалуйста, выберите другое имя.")
