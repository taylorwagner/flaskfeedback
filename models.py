from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect db to Flask app"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, unique=True)

    password = db.Column(db.Text, nullable=False)

    email = db.Column(db.String(50), nullable=False, unique=True)

    first_name = db.Column(db.String(30), nullable=False)

    last_name = db.Column(db.String(30), nullable=False)

    feedbacks = db.relationship('Feedback', backref='user', cascade='all, delete')


    #start_register
    @classmethod
    def register(cls, username, password, first_name, last_name, email):
        """Register user with hashed pw & return user info"""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        user = cls(username=username, password=hashed_utf8, first_name=first_name, last_name=last_name, email=email)

        db.session.add(user)
        return user
    #end_register

    #start_authenticate
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & pw is correct.
        Return user if valid; else return False"""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u
        else: 
            return False
    #end_authenticate
    
    @property
    def full_name(self):
        """Return full name of the user"""

        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        u = self
        return f"<User username={u.username} password={u.password} email={u.email} first_name={u.first_name} last_name={u.last_name}>"


class Feedback(db.Model):
    __tablename__ = "feedbacks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(100), nullable=False)

    content = db.Column(db.Text, nullable=False)

    username = db.Column(db.String, db.ForeignKey('users.username'))

    
    def __repr__(self):
        f = self
        return f"<Feedback id={f.id} title={f.title} content={f.content} username={f.username}>"