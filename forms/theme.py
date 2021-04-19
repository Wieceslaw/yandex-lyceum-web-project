from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class ThemeForm(FlaskForm):
    name = StringField('Theme name', validators=[DataRequired()])
    submit = SubmitField('Submit')