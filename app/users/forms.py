from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Regexp
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=18),
                        Regexp('^[A-Za-z][A-Za-z0-9_.]*$',
                        message="Username should contain only latin letters, arabic numbers, dots and underscores")])

    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])

    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=50)])

    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=50)])

    #remember = BooleanField('Remember Me')

    submit = SubmitField('Log In')