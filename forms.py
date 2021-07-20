from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import PasswordField, TextField
from wtforms.validators import InputRequired, Email, Length

class AddNewUserForm(FlaskForm):
    """Create form for a new user"""
    username = StringField("Create a Username", validators=[InputRequired("Must create a username for your account!"), Length(max=20)])
    password = PasswordField("Create a Password", validators=[InputRequired("Must create a password for your account!")])
    email = StringField("Email Address", validators=[InputRequired("Must attach an active email address to your account"), Email(), Length(max=50)])
    first_name = StringField("First Name", validators=[InputRequired("Please include your first name for the account"), Length(max=30)])
    last_name = StringField("Last Name", validators=[InputRequired("Please include your last name for the account"), Length(max=30)])


class LoginUserForm(FlaskForm):
    """Log user into App"""
    username = StringField("Create a Username", validators=[InputRequired("Must create a username for your account!"), Length(max=20)])
    password = PasswordField("Create a Password", validators=[InputRequired("Must create a password for your account!")])


class NewFeedbackForm(FlaskForm):
    """Create new feedback"""
    title = StringField("Title of Feedback", validators=[InputRequired("Must include a title"), Length(max=100)])
    content = TextField("Content of Feedback", validators=[InputRequired("Must include content")])


class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""