from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):
    text = TextAreaField('Write', validators=[DataRequired()])
    image = FileField('Add image')
    submit = SubmitField('Comment')