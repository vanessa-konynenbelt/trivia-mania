#models 
from myapp import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
#allows to set up isAuthenticate etc 
from flask_login import UserMixin
from datetime import datetime

#login management 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Trivia', backref='author', lazy=True)

    # Relationships will go here
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    #going to use this in our login view 
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f"Username {self.username}"

class Trivia(db.Model):
    __tablename__ = 'trivias'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, title, user_id):
        self.title = title
        self.user_id = user_id

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    trivia_id = db.Column(db.Integer, db.ForeignKey('trivias.id'), nullable=False)

    def __init__(self, question, answer, trivia_id):
        self.question = question
        self.answer = answer
        self.trivia_id = trivia_id
