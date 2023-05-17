
from datetime import date
from src.main import db


class Book(db.Model):
    """Book model"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    published = db.Column(db.Integer)
    genre = db.Column(db.String(255), default=None)
    image_link = db.Column(db.String(255))

   

def new_book(author: str, title: str, image_link: str, published: int, genre: str):
    db.add(Book(author=author, title=title, image_link=image_link,published = published, genre=genre))
    db.commit()
    
    return True
