import os
from pprint import pprint
from flask import Blueprint, current_app, redirect, render_template,flash, url_for,request
from flask_login import login_required
from werkzeug.utils import secure_filename
from  werkzeug.datastructures.file_storage import FileStorage
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
    form = BookForm()
    
    if form.validate_on_submit():
    
        book = Book.query.filter_by(name = form.name.data).first()
        if book:
            flash('Book Already Found in Database', 'danger')
        else:
            
            image_file = form.image_link.data
            image_filename = secure_filename(image_file.filename)
            # image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(f"src/static/files/{image_filename}")
            db.session.add(  
                Book(
                    name=form.name.data,
                    author=form.author.data,
                    published=form.published.data,
                    genre=Genre(form.genre.data),
                    description= form.description.data, 
                    in_stock = form.in_stock.data ,
                    show = True if form.show.data == 'Yes'  else  False,
                    image_link=f"files/{image_filename}"
                )
            )
            db.session.commit()
            flash('Book Added Successfully', 'success')
            return redirect(url_for('admin.add_book'))
            
       

    return render_template('admin/book.html', title='Add Book', form=form)

@admin.route("/book/edit/<int:book_id>", methods=['GET', 'POST'])
@login_required
@role_required(Role.ADMIN)
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookUpdateForm(obj=book)
    
    
    if form.validate_on_submit():
       
        print(type(form.image_link.data))
        book.name = form.name.data if form.name.data != book.name else book.name
        book.author = form.author.data if form.author.data != book.author else book.author
        book.published = form.published.data if form.published.data != book.published else book.published
        book.genre = form.genre.data if form.genre.data != book.genre else book.genre
        book.description = form.description.data if form.description.data != book.description else book.description
        book.in_stock = form.in_stock.data if form.in_stock.data != book.in_stock else book.in_stock
        if form.show.data == str(True):
           book.show = True  if form.show.data != str(book.show) else book.show
        else: 
             book.show = False  if form.show.data != book.show else book.show
        if type(form.image_link.data) == FileStorage:
            image_file = form.image_link.data
            image_filename = secure_filename(image_file.filename)
            # image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(f"src/static/files/{image_filename}")
            book.image_link = f"files/{image_filename}" if f"files/{image_filename}" != book.image_link else book.image_link
         
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

