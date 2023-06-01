import os
from pprint import pprint
import uuid
from flask import Blueprint, current_app, redirect, render_template, flash, session, url_for, request
from flask_login import login_required
from werkzeug.utils import secure_filename
from werkzeug.datastructures.file_storage import FileStorage
from src.extensions.admin_login_required import admin_login_required
from src.models.user import Role, Admin, AccessKey
from src.models.books import Book, Genre
from src.forms.book import BookForm, BookUpdateForm
from src.forms.login import AdminRegisterForm, AdminLoginForm
from src.main import db

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if session['admin_logged_in'] == True:
        return redirect(url_for('admin.dashboard'))
    form = AdminLoginForm()

    if form.validate_on_submit():

        user = Admin.query.filter_by(email=form.email.data).first()

        if user and user.password == form.password.data:
            session['admin_logged_in'] = True

            return redirect(url_for('admin.dashboard'))

        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
            # return redirect(url_for('admin.register'))
    return render_template('admin/login.html', title='Login', form=form)


@admin.route("/register", methods=['GET', 'POST'])
def register():
    form = AdminRegisterForm()
    if form.validate_on_submit():
        access_key = AccessKey.query.filter_by(
            key=form.access_key.data, active=True).first()

        if access_key:
            user = Admin.query.filter_by(email=form.email.data).first()
            if not user:
                db.session.add(Admin(
                    email=form.email.data,
                    password=form.password.data,

                )
                )
                db.session.commit()
                session['admin_logged_in'] = True
                flash('Successfully Registered', 'success')
                return redirect(url_for('admin.dashboard'))
            else:
                flash('Admin Already Registered. Please Login', 'warning')
                return redirect(url_for('admin.login'))
        else:
            flash('Incorrect Access Key', 'error')

    return render_template('admin/register.html', title='Register', form=form)


@admin.route("/logout")
def logout():
    session['admin_logged_in'] = False

    return redirect(url_for('admin.login'))


@admin.route('/access-key', methods=['GET', 'POST'])
@admin_login_required
def create_access_key():
    if request.method == 'POST':
        # Generate a new admin key
        # Replace this with your own key generation logic
        key = str(uuid.uuid4())

        # Create a new AdminKey instance
        admin_key = Admin(key=key, active=True)

        # Add the key to the database
        db.session.add(admin_key)
        db.session.commit()
        flash("New Access Token Create : " + key, "success")
        # Redirect back to the same route to refresh the page
        return redirect(url_for('admin.create_access_key'))

    admins = Admin.query.all()
    return render_template('admin/all_admin.html', admins=admins)


@admin.route('/access-key/delete/<int:id>')
@admin_login_required
def delete_access_key(id):
    admin = Admin.query.get_or_404(id)
    db.session.delete(admin)
    db.session.commit()
    flash('Admin deleted.', "warning")
    return redirect(url_for('admin.create_access_key'))


@admin.route('/')
@admin_login_required
def dashboard():
    book = Book.query.all()
    pprint([i.__dict__ for i in book])
    return render_template('admin/admin.html', title='Admin', books=book)


@admin.route("/book/add", methods=['GET', 'POST'])
@admin_login_required
def add_book():
    form = BookForm()

    if form.validate_on_submit():

        book = Book.query.filter_by(name=form.name.data).first()
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
                    description=form.description.data,
                    in_stock=form.in_stock.data,
                    show=True if form.show.data == 'Yes' else False,
                    image_link=f"files/{image_filename}"
                )
            )
            db.session.commit()
            flash('Book Added Successfully', 'success')
            return redirect(url_for('admin.add_book'))

    return render_template('admin/book.html', title='Add Book', form=form)


@admin.route("/book/edit/<int:book_id>", methods=['GET', 'POST'])
@admin_login_required
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookUpdateForm(obj=book)
    has_changes = False

    if form.validate_on_submit():
        if form.name.data != book.name:
            print(form.name.data)
            book.name = form.name.data
            has_changes = True

        if form.author.data != book.author:
            print(form.author.data)
            book.author = form.author.data
            has_changes = True

        if form.published.data != book.published:
            print(form.published.data)
            book.published = form.published.data
            has_changes = True

        if form.genre.data != book.genre and form.genre.data != Genre.NonCategorized:
            print(form.genre.data)
            book.genre = form.genre.data
            has_changes = True

        if form.description.data != book.description:
            print(form.description.data)
            book.description = form.description.data
            has_changes = True

        if form.in_stock.data != book.in_stock:
            book.in_stock = form.in_stock.data
            has_changes = True

        if form.show.data != str(book.show):
            if form.show.data == str(True):
                print(form.show.data)
                book.show = True
                has_changes = True
            else:
                print(form.show.data)
                book.show = False
                has_changes = True

        if isinstance(form.image_link.data, FileStorage):
            print(form.image_link.data)
            image_file = form.image_link.data
            image_filename = secure_filename(image_file.filename)
            image_file.save(f"src/static/files/{image_filename}")
            new_image_link = f"files/{image_filename}"
            if new_image_link != book.image_link:
                book.image_link = new_image_link
                has_changes = True

        if has_changes:

            db.session.commit()
            flash('Book Updated Successfully', 'success')
        else:
            flash('No changes made to the book', 'info')

    return render_template('admin/book.html', title='Edit Book', form=form)


@admin.route('/book/delete/<int:id>', methods=['POST'])
@admin_login_required
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted.', "danger")
    return redirect(url_for('admin.dashboard'))
