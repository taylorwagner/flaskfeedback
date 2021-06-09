from flask import Flask, redirect
from flask.templating import render_template
from models import db, connect_db, User, Feedback
from forms import AddNewUserForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "santanarush"

connect_db(app)
db.create_all()


@app.route('/')
def redirect_home():
    """Redirect to /register"""

    return redirect('/register')


@app.route('/register')
def get_register_form():
    """Show a form that when submitted will register/create a user. This form should accept a username, password, email, first_name, and last_name."""

    form = AddNewUserForm()

    return render_template('register.html', form=form)