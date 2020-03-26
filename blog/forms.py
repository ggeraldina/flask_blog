""" Forms """
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    """ post """
    title = StringField(label="Название: ",
                        validators=[DataRequired(), Length(max=200)],
                        id="id_title")
    text = TextAreaField(label="Текст: ", validators=[DataRequired], id="id_title")
    instance = None


    # def __init__(self, post=None, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     if post is not None:
    #         self.instance = post
    #         self._copy_data_to_form()

    # def _copy_data_to_form(self):
    #     self.title.data = self.instance.title
    #     self.text.data = self.instance.text
