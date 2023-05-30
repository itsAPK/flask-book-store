from pprint import pprint
from flask import Blueprint, redirect, render_template,flash, url_for,request
from flask_login import login_required

from src.models.user import Role
from src.extensions.check_user_role import role_required
from src.models.books import Book, Genre
from src.forms.book import BookForm,BookUpdateForm
from src.main import db

admin = Blueprint('admin', __name__,url_prefix='/admin')


@admin.route('/')
@login_required
@role_required(Role.ADMIN)
def dashboard():
    book = Book.query.all()
    pprint([i.__dict__ for i in book])
    return  render_template('admin/admin.html', title='Admin', books=book)

@admin.route("/book/add", methods=['GET', 'POST'])
@login_required
@role_required(Role.ADMIN)
def add_book():
    form = BookForm(request.form)
  
    if form.validate_on_submit():
        
        db.session.add(  
            Book(
                name=form.name.data,
                author=form.author.data,
                published=form.published.data,
                genre=Genre(form.genre.data),
                description= form.description.data, 
                in_stock = form.in_stock.data ,
                show = True if form.show.data == 'Yes'  else  False,
                image_link=form.image_link.data
            )
        )
        db.session.commit()
        flash('Book Added Successfully', 'success')

    return render_template('admin/book.html', title='Add Book', form=form)

@admin.route("/book/edit/<int:book_id>", methods=['GET', 'POST'])
@login_required
@role_required(Role.ADMIN)
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookUpdateForm(request.form,obj=book)
    if form.validate_on_submit():
        
        
        book.name = form.name.data if form.name.data != book.name else book.name
        book.author = form.author.data if form.author.data != book.author else book.author
        book.published = form.published.data if form.published.data != book.published else book.published
        book.genre = form.genre.data if form.genre.data != book.genre else book.genre
        book.description = form.description.data if form.description.data != book.description else book.description
        book.in_stock = form.in_stock.data if form.in_stock.data != book.in_stock else book.in_stock
        book.show = True if book.show == "True" else False if form.show.data != book.show else book.show
        book.image_link = form.image_link.data if form.image_link.data != book.image_link else book.image_link
         
        db.session.commit()
        flash('Book Updated Successfully', 'success')

    return render_template('admin/book.html', title='Edit Book', form=form)



@admin.route('/book/delete/<int:id>', methods=['POST'])
@login_required
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted.',"danger")
    return redirect(url_for('admin.dashboard'))

