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

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()
        
    
        
    from src.routes.auth import auth
    from src.routes.home import main
    
    app.register_blueprint(auth)
    app.register_blueprint(main)

    return app
