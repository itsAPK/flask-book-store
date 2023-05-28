

import datetime
from pprint import pprint
from flask import Blueprint, redirect, render_template,flash, url_for,request
from flask_login import login_required
from src.models.books import Book
from src.forms.book import BookForm
from src.main import db

book = Blueprint('books', __name__)




@book.route('/book/<int:book_id>',methods=['GET'])
@login_required
def get_book(book_id):
    book = Book.query.get_or_404(book_id)
   
    if not book:
         flash("Book Not Found in Database","error")
         return redirect(url_for('home.home'))
    

    return render_template('book.html', title=book.name, book=book)

    