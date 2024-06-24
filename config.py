#!/usr/bin/python3
"""Application Configuration"""
import os


class Config:
    """Configuration Class"""
    SECRET_KEY = 'mysecretkey'
    SQLALCHEMY_DATABASE_URI ='mysql://kipchumba:1Laflame_@localhost/talento'
    SQLALCHEMY_TRACK_MODIFICATION = False
