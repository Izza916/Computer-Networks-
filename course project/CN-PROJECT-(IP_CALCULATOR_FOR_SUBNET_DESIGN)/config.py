import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
    WTF_CSRF_ENABLED = True
    DEBUG = True
