#!/usr/bin/python3
"""Class model for users"""
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    """Users model"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    about = db.Column(db.String(255), nullable=False)
    profile_photo = db.Column(db.String(255))
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    events = db.relationship('Event', backref='user', lazy=True)