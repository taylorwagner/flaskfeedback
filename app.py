from flask import Flask, redirect, flash, session
from flask.templating import render_template
from werkzeug.exceptions import Unauthorized


from models import db, connect_db, User, Feedback
from forms import AddNewUserForm, LoginUserForm, NewFeedbackForm, DeleteForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "santanarush"

connect_db(app)
# db.create_all()


@app.route('/')
def redirect_home():
    """Redirect to /register"""

    return redirect('/register')


# redundant -- not needed
# @app.route('/register')
# def get_register_form():
#     """Show a form that when submitted will register/create a user. This form should accept a username, password, email, first_name, and last_name."""

#     form = AddNewUserForm()

#     return render_template('register.html', form=form)


@app.route('/secret')
def secret():
    """Example hidden page for logged-in users only."""

    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")

        # alternatively, can return HTTP Unauthorized status:
        #
        # from werkzeug.exceptions import Unauthorized
        # raise Unauthorized()

    else:
        return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Process the registration form by adding a new user. Then redirect to /secret"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = AddNewUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, first_name, last_name, email)

        db.session.commit()

        session["username"] = new_user.username

        flash(f"Thanks for registering, {first_name} {last_name}! The user you created has been registered as: {username}. Make sure you write down your password and keep it in a safe place.")
        return redirect(f"/users/{new_user.username}")

    else:
        return render_template(
            "register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Show and handle form for logging in a user"""

    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Invalid username or password"]
            return render_template("login.html", form=form)

    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("username")

    return redirect("/login")


@app.route('/users/<username>')
def profile(username):
    """Display a template the shows information about that user (everything except for their password)"""
    if "username" not in session or username != session['username']:
        raise Unauthorized()
        # flash("You must be logged in to view!")
        # return redirect("/")

    else:
        user = User.query.get_or_404(username)
        form = DeleteForm()

        return render_template('profile.html', user=user, form=form)


@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Remove user nad redirect to login."""
    if "username" not in session or username != session['username']:
        raise Unauthorized()
        # flash("You must be logged in to view!")
        # return redirect("/")

    else:
        user = User.query.get_or_404(username)
        db.session.delete(user)
        db.session.commit()
        session.pop("username")

        return redirect('/login')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """Show add-feedback form and process it."""
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = NewFeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("newfeedback.html", form=form)


@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """Show update-feedback form and process it."""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = NewFeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()
        
        return redirect(f"/users/{feedback.username}")

    return render_template("editfeedback.html", feedback=feedback, form=form)


# @app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
# def delete_feedback(feedback_id):
#     if "user_id" not in session:
#         flash("You must be logged in to view!")
#         return redirect('/')