#!/usr/bin/python3
"""Application Configuration"""
import os


class Config:
    """Configuration Class"""
    SECRET_KEY = 'mysecretkey'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'mysql://kipchumba:1Laflame_@localhost/talento')
    SQLALCHEMY_TRACK_MODIFICATION = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'victorkipchumba039@gmail.com'
    MAIL_PASSWORD = 'howv zrbi jiyj aldi'
    UPLOAD_FOLDER = './app/static/images/uploads'