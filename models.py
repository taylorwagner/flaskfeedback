from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

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

    
    # @property
    # def full_name(self):
    #     """Return full name of the user"""

    #     return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        u = self
        return f"<User username={u.username} password={u.password} email={u.email} first_name={u.first_name} last_name={u.last_name}>"