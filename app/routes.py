#!/usr/bin/python3
"""This module contains all the routes required by the web app
"""
from app.models.user import User
from app.models.event import Event
from app.models.photo import Photo
from app import db, mail
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, flash, current_app as app
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer
import os
import re

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def is_valid_email(email):
    '''Basic regex for email validation'''
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid credentials', 'error')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('account'))

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        about = request.form['about']
        email = request.form['email']
        password = request.form['password']
        profile_photo = request.files['profile_photo']

        if User.query.filter_by(username=username).first():
            flash('Username Taken', 'error')
            return redirect(url_for('register'))
        if User.query.filter_by(email=email).first():
            flash('User Already Exists', 'error')
            return redirect(url_for('register'))
        
        if profile_photo:
            profile_filename = secure_filename(profile_photo.filename)
            profile_photo_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_filename)
            profile_photo.save(profile_photo_path)

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, about=about,
                         profile_photo=profile_filename, email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('User registered successfully', 'success')
        return redirect(url_for('login'))

    return render_template('sign-up.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/profile/<username>')
def profile(username):
    '''This route Displays Profile of the user who uploaded the photos
        Event orgarnizer or Photo grapher
    '''
    user = User.query.filter_by(username=username).first()
    events = user.events
    event_count = len(events)
    photo_count = sum(len(event.photos) for event in events)
    return render_template('profile.html', user=user, events=events,
                            event_count=event_count, photo_count=photo_count)

@app.route('/logout')
@login_required
def logout():
    '''This Route Logouts a user'''
    logout_user()
    return redirect(url_for('login'))

@app.route('/forgot', methods=['POST', 'GET'])
def forgot():
    '''Request for password reset link
    '''
    if request.method == 'POST':
        email = request.form['email'].strip()

        if not is_valid_email(email):
            flash('Invalid email address format', 'error')
            return redirect(url_for('forgot'))

        user = User.query.filter_by(email=email).first()

        if user:
            token = s.dumps(user.email, salt='password-reset-salt')
            reset_url = url_for('reset', token=token, _external=True)
            subject = "Password Reset"
            sender = app.config['MAIL_USERNAME']
            recipients = [user.email]
            body = f"Please click the link to reset password: {reset_url}"

            msg = Message(subject=subject, sender=sender, recipients=recipients)
            msg.body = body
            mail.send(msg)

            flash('Password reset link sent to email', 'info')
        else:
            flash('Email is not registered. Try again', 'error')
        return redirect(url_for('forgot'))
    
    return render_template('forgot-password.html')

@app.route('/reset/<token>', methods=['POST', 'GET'])
def reset(token):
    '''Reset password route'''
    try:
        email = s.loads(token, salt='password-reset-salt', max_age=3600)
    except Exception as e:
        flash('Password reset link is invalid or expired', 'error')
        return redirect(url_for('forgot'))
    
    if request.method == 'POST':
        new_pwd = request.form['new-pwd']
        confirm_pwd = request.form['confirm-pwd']
    
        if new_pwd != confirm_pwd:
            flash('Passwords do not match!', 'error')
            return redirect(url_for('reset', token=token))
        
        user = User.query.filter_by(email=email).first()
        hashed_password = generate_password_hash(new_pwd, method='pbkdf2:sha256')
        user.password = hashed_password
        db.session.commit()

        flash('Password Reset Successful!', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset-password.html', token=token)

@app.route('/collection/<event_id>')
def collection(event_id):
    '''Displays collections of photos uploaded by user for the event'''
    photos = Photo.query.filter_by(event_id=event_id).all()
    event = Event.query.get_or_404(event_id)
    print(event)
    return render_template('collection.html', photos=photos, event=event)

@app.route('/account')
@login_required
def account():
    """Displays Account details to A user
    """
    events = Event.query.filter_by(user_id=current_user.id).all()
    event_count = len(events)
    photo_count = sum(len(event.photos) for event in events)
    return render_template('account.html', events=events, event_count=event_count, photo_count=photo_count)

@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    """Creates an event
    """
    if request.method == 'POST':
        name = request.form['name']
        about = request.form['about']
        cover_photo = request.files['cover']
        photos = request.files.getlist('photos')
        price = request.form['price']

        if cover_photo:
            cover_filename = secure_filename(cover_photo.filename)
            cover_photo_path = os.path.join(app.config['UPLOAD_FOLDER'], cover_filename)
            cover_photo.save(cover_photo_path)
        
        new_event = Event(name=name, about=about, cover_photo=cover_filename,
                           user_id=current_user.id)
        db.session.add(new_event)
        db.session.commit()

        for photo in photos:
            if photo:
                photo_filename = secure_filename(photo.filename)
                photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
                photo.save(photo_path)

                new_photo = Photo(file_path=photo_filename, event_id=new_event.id, price=price)
                db.session.add(new_photo)

        db.session.commit()
        return redirect(url_for('account'))
    
    return render_template('create_event.html')

@app.route('/home')
def home():
    """Home route the home page of the web app
    """
    events = Event.query.limit(10).all()
    return render_template('home.html', events=events)

@app.route('/event/<event_id>')
def event(event_id):
    """Displays event details
    """
    photos = Photo.query.filter_by(event_id=event_id).all()
    event = Event.query.get_or_404(event_id)
    creator = event.user
    print(event)
    return render_template('event.html', photos=photos, event=event, creator=creator)

@app.route('/check-out')
def checkout():
    return render_template('checkout.html')