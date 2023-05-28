
from datetime import date
import datetime
import enum
from src.main import db


class Status(enum.Enum):

    BORROWED = 'BORROWED'
    RETURNED = 'RETURNED'
    
class Genre(enum.Enum):
    NonCategorized = 'Non-Categorized'
    Fiction = 'Fiction'
    Non_fiction = 'Non-fiction'
    Mystery = 'Mystery'
    Thriller = 'Thriller'
    Science_Fiction = 'Science Fiction'
    Fantasy = 'Fantasy'
    Romance = 'Romance'
    Historical_Fiction = 'Historical Fiction'
    Horror = 'Horror'
    Biography = 'Biography'
    Autobiography = 'Autobiography'
    Self_help = 'Self-help'
    Travel = 'Travel'
    Poetry = 'Poetry'
    Drama = 'Drama'
    Comedy = 'Comedy'
    Satire = 'Satire'
    Adventure = 'Adventure'
    Childrens = "Childrens"
    Young_Adult = 'Young Adult'
    Graphic_Novels = 'Graphic Novels'
    Crime = 'Crime'
    Western = 'Western'
    Paranormal = 'Paranormal'
    Dystopian = 'Dystopian'
    Memoir = 'Memoir'
    Science = 'Science'
    Philosophy = 'Philosophy'
    Religion = 'Religion'
    Art = 'Art'
    Cookbooks = 'Cookbooks'
    Business = 'Business'
    Economics = 'Economics'
    Politics = 'Politics'
    Sociology = 'Sociology'
    Psychology = 'Psychology'
    Anthologies = 'Anthologies'
    Essays = 'Essays'
    Guidebooks = 'Guidebooks'
   


class Book(db.Model):
    """Book model"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)
    published = db.Column(db.Integer)
    genre = db.Column(db.Enum(Genre), default=Genre.NonCategorized)
    description = db.Column(db.String(255), nullable=False)
    in_stock = db.Column(db.Integer, default=0)
    image_link = db.Column(db.String(255))
    show = db.Column(db.Boolean, default=True)
    borrowed_history = db.relationship('Rental', backref='book')
    
    @db.validates('genre')
    def validate_genre(self, key, value):
        print(value)
        if value not in Genre.__members__.values():
            raise ValueError('Invalid genre value')
        return value


class Rental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    date_borrowed = db.Column(db.DateTime, default=datetime.datetime.now)
    due_date = db.Column(db.DateTime)
    sataus = db.Column(db.Enum(Status), default=Status.BORROWED)
    fine = db.Column(db.Integer, default=0)

