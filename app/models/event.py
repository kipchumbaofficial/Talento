#!/usr/bin/python3
"""Class model for event to store events details
"""
from app import db

class Event(db.Model):
    """Events Model"""
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    about = db.Column(db.String(255), nullable=False)
    cover_photo = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    photos = db.relationship('Photo', backref='event', lazy=True)