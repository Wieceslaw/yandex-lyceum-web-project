from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class MessageForm(FlaskForm):
    text = TextAreaField('Write', validators=[DataRequired()])
    submit = SubmitField('Comment')