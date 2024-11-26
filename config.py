import os, datetime
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_UR')
    # config.py
    CELERY_CONFIG = {
    "broker_url": os.getenv('BROKER_URL'),
    "result_backend": os.getenv('RESULT_BACKEND')
}

    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True


password = os.getenv('EMAIL_PASSWORD')
sender_email = os.getenv('SENDER_EMAIL')
