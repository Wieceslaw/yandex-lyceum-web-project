from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    nickname = StringField('Nickname', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')