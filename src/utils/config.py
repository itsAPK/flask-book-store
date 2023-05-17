"""Application configuration."""

import os 
from dotenv import load_dotenv

load_dotenv()  

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', "secret_key")
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL',
                                             'mysql+pymysql://flaskbook_readyquite:ba5ecb027ea80c6b33221d1b69b82772ebe6ecd2@db0.h.filess.io:3307/flaskbook_readyquite')
