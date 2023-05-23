

from flask import Blueprint, redirect, render_template,flash, url_for
from flask_login import login_required
from src.models.books import Book
from src.forms.book import BookForm
from src.main import db

book = Blueprint('book', __name__)


@book.route("/book/add", methods=['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
    if form.validate_on_submit():

        db.session.add(  
            Book(
                name=form.name.data,
                author=form.author.data,
                published=form.published.data,
                genre=form.genre.data,
                image_link=form.image_link.data
            )
        )
        db.session.commit()
        flash('Book Added Successfully', 'success')

    return render_template('book.html', title='Add Book', form=form)


@book.route('/book/delete/<int:book_id>', methods=['POST'])
@login_required
def delete(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted.',"danger")
    return redirect(url_for('home.home'))