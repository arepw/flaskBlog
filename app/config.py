import os
from flask_security import uia_username_mapper, uia_email_mapper

BASE_DIR = os.path.dirname(os.path.abspath(__name__))


class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data.db'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'data.db')
    # having issues with path as because alembic creates db inside app folder
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    SECURITY_PASSWORD_HASH = 'sha512_crypt'
    SECURITY_REGISTERABLE = True
    SECURITY_USER_IDENTITY_ATTRIBUTES = [{"username": {"mapper": uia_username_mapper, "case_insensitive": False}},
                                        {"email": {"mapper": uia_email_mapper, "case_insensitive": True}}]
    SECURITY_USERNAME_ENABLE = True
    SECURITY_USERNAME_REQUIRED = True
    SECURITY_CONFIRMABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_POST_CHANGE_VIEW = '/profile'
    SECURITY_RECOVERABLE = True
    SECURITY_RESET_URL = '/recover'
    """
    I don't know why, but by default after registration users are redirected
    to "/", although SECURITY_CONFIRMABLE equals True, so user must confirm
    registration via link. Flask-Security shows message about it BUT it is in
    the "register" view. So I specified SECURITY_POST_REGISTER_VIEW to "/register"
    for better user experience.
    """
    SECURITY_POST_REGISTER_VIEW = '/register'
    # MAIL CONFIG
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = MAIL_USERNAME
    SECURITY_EMAIL_SENDER = MAIL_USERNAME
