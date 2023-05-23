# -*- coding: utf-8 -*-

"""Main Application"""

from flask_login import LoginManager
from flask import Flask
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


from src.utils.config import Config

logging.basicConfig(level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__,template_folder='../src/templates/')
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///main.db"

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    

    with app.app_context():
        from .models.user import User
        from .models.books import Book
        db.create_all()
        
    #     books = [
    #     Book(name='To Kill a Mockingbird', author="Lee Harper", published="2016", genre="Classic",
    #          image_link="https://cdn.asaha.com/assets/thumbs/b95/b9516f63a1b8f1d7944695d00f4604b8.jpg"),
    #    Book(name='To Kill a Mockingbird', author="Lee Harper", published="2016", genre="Classic",
    #          image_link="https://cdn.asaha.com/assets/thumbs/b95/b9516f63a1b8f1d7944695d00f4604b8.jpg"),
    #     ]
    #     db.session.add_all(books)
    #     db.session.commit()
        
        
        # db.session.add(User(email = "user@example.com", password = "password"))
        # db.session.commit()
    
        
    from src.routes.auth import auth
    from src.routes.home import main
    from src.routes.books import book
    
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(book)

    return app
