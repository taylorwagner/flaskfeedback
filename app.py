from flask import Flask, redirect, flash, session
from flask.templating import render_template
from models import db, connect_db, User, Feedback
from forms import AddNewUserForm, LoginUserForm

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


@app.route('/register', methods=['GET', 'POST'])
def add_user():
    """Process the registration form by adding a new user. Then redirect to /secret"""

    form = AddNewUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        hash_pw = User.register(username, password)

        new_user = User(username=username, password=hash_pw, email=email, first_name=first_name, last_name=last_name)

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id

        flash(f"Thanks for registering, {first_name} {last_name}! The user you created has been registered as: {username}. Make sure you write down your password and keep it in a safe place.")
        return redirect("/secret")

    else:
        return render_template(
            "register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["user_id"] = user.id
            return redirect('/secret')

        else:
            form.username.errors = ["Bad username/password"]

    return render_template('login.html', form=form)