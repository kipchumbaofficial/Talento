#!/usr/bin/python3
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

from app.models.user import User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    with app.app_context():
        from . import routes  # Ensure routes are imported within the app context
        db.create_all()
    
    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
