#!/usr/bin/python3
"""Application Configuration"""
import os


class Config:
    """Configuration Class"""
    SECRET_KEY = 'mysecretkey'
    SQLALCHEMY_DATABASE_URI ='postgresql+psycopg2://kipchumba:YVClqooC0o3A79Fuy2LfF5afuRWXmUOQ@dpg-cq0ivb3v2p9s73cb1j5g-a/talento'
    SQLALCHEMY_TRACK_MODIFICATION = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'victorkipchumba039@gmail.com'
    MAIL_PASSWORD = 'howv zrbi jiyj aldi'
    UPLOAD_FOLDER = './app/static/images'
