from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, IntegerField, SelectField #wtforms is a package
from wtforms.fields import DateTimeLocalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, Optional #DataRequired is a class we are importing
from flask_wtf.file import FileField, FileAllowed
from event_finder.models import User #only user is imported for validation purposes


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

class UpdateAccountForm(FlaskForm):
    picture = FileField('Update profile picture', validators=[FileAllowed(['jpg', 'png'])])
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField ('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose another one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError('That email is taken. Please choose another one.')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    event_date = DateTimeLocalField('Date and Time', format="%Y-%m-%dT%H:%M", validators=[DataRequired()])
    duration_minutes = IntegerField('Duration (min)', validators=[Optional(), NumberRange(min=1, max=1440)])
    picture = FileField('Upload a picture of your event', validators=[FileAllowed(['jpg', 'png'])])
    content = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField(choices=[(0, 'All'),
        (7, 'Arts and crafts'),
        (2, 'Boardgames'),
        (3, 'Dancing'),
        (4, 'Demo'),
        (5, 'Food'),
        (6, 'Meetup'),
        (1, 'Music'),
        (8, 'Party'),
        (9, 'Soliparty'),
        (10, 'Sports'),
        (11, 'Tandem'),
        (12, 'Other')], coerce=int)
    submit = SubmitField('Post')

class PostFilterForm(FlaskForm):
    title_word = StringField('Word in Title')
    city = StringField('City')
    category = SelectField(choices=[(0, 'All'),
        (7, 'Arts and crafts'),
        (2, 'Boardgames'),
        (3, 'Dancing'),
        (4, 'Demo'),
        (5, 'Food'),
        (6, 'Meetup'),
        (1, 'Music'),
        (8, 'Party'),
        (9, 'Soliparty'),
        (10, 'Sports'),
        (11, 'Tandem'),
        (12, 'Other')], coerce=int)
    submit = SubmitField()