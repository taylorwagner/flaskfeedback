from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField
from wtforms.fields.html5 import EmailField
from wtforms.fields.simple import PasswordField
from wtforms.validators import InputRequired, Email, Length
import email_validator

class AddNewUserForm(FlaskForm):
    """Create form for a new user"""
    username = StringField("Create a Username", validators=[InputRequired("Must create a username for your account!"), Length(max=20)])
    password = PasswordField("Create a Password", validators=[InputRequired("Must create a password for your account!")])
    email = EmailField("Email Address", validators=[InputRequired("Must attach an active email address to your account"), Email(), Length(max=50), email_validator])
    first_name = StringField("First Name", validators=[InputRequired("Please include your first name for the account"), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired("Please include your last name for the account"), Length(max=30)])
    #need to verify email part of the form -- how to implement the email_validator that is imported on line 7