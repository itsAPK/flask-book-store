from src.main import db
from flask_login import UserMixin
from enum import Enum
class Role(Enum):
    USER = 'user'
    ADMIN = 'admin'
    



class User(db.Model,UserMixin):
    """User Model"""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    borrowed_books =  db.relationship('Rental', backref='user')
    role = db.Column(db.Enum(Role), nullable=False, default=Role.USER)