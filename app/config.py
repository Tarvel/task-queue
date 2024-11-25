import os, datetime
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    # config.py
    CELERY_CONFIG = {
    "broker_url": os.getenv('BROKER_URL'),  # Use 'redis', the service name, instead of 'localhost'
    "result_backend": os.getenv('RESULT_BACKEND')
}

    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
