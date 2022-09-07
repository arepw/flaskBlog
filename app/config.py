import os

BASE_DIR = os.path.dirname(os.path.abspath(__name__))


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data.db')
    # having issues with path as because alembic creates db inside app folder
    SQLALCHEMY_TRACK_MODIFICATIONS = False
