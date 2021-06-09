from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField
from wtforms.fields.simple import PasswordField
from wtforms.validators import InputRequired, Email

class AddNewUserForm(FlaskForm):
    """Create form for a new user"""
    username = StringField("Create a Username", validators=[InputRequired("Must create a username for your account!")])
    password = PasswordField("Create a Password", validators=[InputRequired("Must create a password for your account!")])
    email = StringField("Email Address", validators=[InputRequired("Must attach an active email address to your account"), Email()])
    first_name = StringField("First Name", validators=[InputRequired("Please include your first name for the account")])
    last_name = StringField("Last Name", validators=[InputRequired("Please include your last name for the account")])
# Need to include length maximums