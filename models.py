from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
  __tablename__ = 'users'

  username = db.Column(db.String(20), primary_key=True, unique=True)
  password = db.Column(db.String, nullable=False)
  email = db.Column(db.String(50), unique=True)
  first_name = db.Column(db.String(30), nullable=False)
  last_name = db.Column(db.String(30), nullable=False)

  def __repr__(self):
    return f'<username: {self.username} password: {self.password} email: {self.email} firstname: {self.first_name } lastname: {self.last_name}>'

  @classmethod
  def register(cls, username, pwd, email, firstname, lastname):
     """Register user into database."""
     hashed = bcrypt.generate_password_hash(pwd)
     hashed_utf8 = hashed.decode("utf8")

     return cls(username=username, password=hashed_utf8, email=email, first_name=firstname, last_name=lastname)

  @classmethod
  def authenticate(cls, username, pwd):
    """Validate credentials via database."""
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, pwd):
      return user
    else:
      return False


class Feedback(db.Model):
  __tablename__ = 'feedback'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  title = db.Column(db.String(100), nullable=False)
  content = db.Column(db.String, nullable=False)
  username = db.Column(db.String(20), db.ForeignKey('users.username'))

  user = db.relationship('User', backref='feedback')