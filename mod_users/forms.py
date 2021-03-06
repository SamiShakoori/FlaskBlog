from flask_wtf import FlaskForm
from wtforms.fields.html5 import EmailField
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    name = StringField(validators=[DataRequired()])
    email = EmailField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    confirm_password = PasswordField(validators=[DataRequired()])
    register = SubmitField()


class LoginForm(FlaskForm):
    email = EmailField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired()])
    login = SubmitField()
