
from datetime import date
import datetime
import enum
from src.main import db


class Status(enum.Enum):

    BORROWED = 'BORROWED'
    RETURNED = 'RETURNED'


class Book(db.Model):
    """Book model"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    published = db.Column(db.Integer)
    genre = db.Column(db.String(255), default=None)
    description = db.Column(db.String(255), nullable=False)
    in_stock = db.Column(db.Boolean, default=True)
    image_link = db.Column(db.String(255))
    borrowed_history = db.relationship('Rental', backref='book')


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    date_borrowed = db.Column(db.DateTime, default=datetime.datetime.now)
    due_date = db.Column(db.DateTime)
    sataus = db.Column(db.Enum(Status), default=Status.BORROWED)
    fine = db.Column(db.Integer, default=0)
