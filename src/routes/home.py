from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from src.main import db, login_manager
from src.models.user import User
from src.models.books import Book

main = Blueprint('home', __name__)


@main.route('/')
def home():
   
    book = Book.query.all()
    return render_template('home.html', title='Home', books=book)
