""" Forms """
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    """ Post """
    title = StringField(label="Название: ",
                        validators=[DataRequired(), Length(max=200)],
                        id="id_title")
    text = TextAreaField(label="Текст: ", validators=[DataRequired()], id="id_text")
