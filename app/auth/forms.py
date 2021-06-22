from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,BooleanField,SubmitField, FileField
from wtforms.validators import Required,Email,Length,EqualTo
from ..models import User
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed, FileRequired

class LoginForm(FlaskForm):
    email = StringField(validators=[Required(),Email()])
    password = PasswordField(validators =[Required()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class SignUpForm(FlaskForm):
    email = StringField('Email Address', validators=[Required(), Email()])
    fname = StringField('First Name', validators=[Required()])
    lname = StringField('Last Name', validators=[Required()])
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[Required(), EqualTo('password_confirm', message='Passwords do not match.')])
    password_confirm = PasswordField('Confirm Password', validators=[Required()])
    profile = FileField('Upload Profile Picture', validators=[FileRequired(), FileAllowed(['jpg','png'], 'Images only allowed.')])
    sub = BooleanField('Subscribe to receive updates about new posts.')
    submit = SubmitField('Sign Up')

    # Validate email
    def validate_email(self, data_field):
        if User.query.filter_by(email=data_field.data).first():
            raise ValidationError('That email has an existing account.')

    # Validate username
    def validate_username(self, data_field):
        if User.query.filter_by(username = data_field.data).first():
            raise ValidationError('Username is taken.')