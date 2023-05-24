from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from src.main import db, login_manager
from src.models.user import User
from src.models.books import Book

main = Blueprint('home', __name__)


@main.route('/')
def home():
    # l = [
    #     Book(name='To Kill a Mockingbird', author="Lee Harper", published="2016", genre="Classic",
    #          image_link="https://cdn.asaha.com/assets/thumbs/b95/b9516f63a1b8f1d7944695d00f4604b8.jpg")
    # ]
    # db.session.add_all(l)
    # db.session.commit()
    book = Book.query.all()
    return render_template('home.html', title='Home', books=book)
