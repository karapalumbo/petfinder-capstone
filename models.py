from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


class User(db.Model):
    """User in the system."""   

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    username = db.Column(db.String(20), nullable=False,  unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    

    @classmethod
    def register(cls, username, password, email, first_name, last_name):

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")
        return cls(
            username=username,
            password=hashed_utf8,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        

    @classmethod
    def authenticate(cls, username, password):
        
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
  
        return False


class Pet(db.Model):
    """pets table."""

    __tablename__ = 'pets'
    id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(30), nullable=True)
    species = db.Column(db.Text, nullable=True)
    gender = db.Column(db.Text, nullable=True)
    age = db.Column(db.Text, nullable=True)
    size = db.Column(db.Text, nullable=True)
    color = db.Column(db.Text, nullable=True)

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


