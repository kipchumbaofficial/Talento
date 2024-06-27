#!/usr/bin/python3
"""Class model for users"""
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    """Users model"""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    events = db.relationship('Event', backref='user', lazy=True)