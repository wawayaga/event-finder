from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField #wtforms is a package
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError #DataRequired is a class we are importing
from event_finder.models import User


class RegistrationForm(FlaskForm):
    #username should have between 2-20 characters
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField ('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose another one.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('That email is taken. Please choose another one.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField ('Log in')