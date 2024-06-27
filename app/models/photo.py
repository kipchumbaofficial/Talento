#!/usr/bin/python3
"""Photo model"""
from app import db


class Photo(db.Model):
    """Photo Model"""
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
