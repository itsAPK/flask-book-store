"""Application configuration."""

import os 
from dotenv import load_dotenv

load_dotenv()  

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', "secret_key")
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
