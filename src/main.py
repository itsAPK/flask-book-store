# -*- coding: utf-8 -*-

"""Main Application"""

import uuid
from flask_login import LoginManager
from flask import Flask
import logging
from flask_sqlalchemy import SQLAlchemy


from src.utils.config import Config
# logging.basicConfig(level=logging.DEBUG,
#                     format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
# logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'



def create_app(config_class=Config):
    app = Flask(__name__,template_folder='../src/templates/')
    app.config.from_object(Config)
    app.config['SQLALCHEMY_DATABASE_URI'] =  "sqlite:///main.db"
    
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    db.init_app(app)
    login_manager.init_app(app)
    
    

    with app.app_context():
        from .models.user import User,Admin
        from .models.books import Book,Rental
        
   
        db.create_all()

        admin_key = Admin.query.first()  # Check if an admin key already exists
        print(admin_key.key)
        if not admin_key:
            # Create a default admin key if none exists
            default_key = Admin(key=uuid.uuid4, active=True)
            db.session.add(default_key)
            db.session.commit()

            print("Admin Key :" + default_key.key)
   
    
        

        
    from src.routes.auth import auth
    from src.routes.home import main
    from src.routes.books import book
    from src.routes.admin import admin as admin_route
    
    app.register_blueprint(auth)
    app.register_blueprint(main)
    app.register_blueprint(book)
    app.register_blueprint(admin_route)


    
    return app
