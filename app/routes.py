#!/usr/bin/python3
from app.models.user import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask import render_template, request, redirect, url_for, flash, current_app as app
from flask_login import login_user, logout_user, login_required, current_user
"""Flask app"""


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
        return redirect(url_for('profile'))

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        if User.query.filter_by(email=email).first():
            flash('User Already Exists', 'error')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(first_name=first_name, last_name=last_name,
                         email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('User registered successfully', 'success')
        return redirect(url_for('login'))

    return render_template('sign-up.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/forgot', methods=['POST', 'GET'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        if User.query.filter_by(email=email).first():
            flash('Password reset link sent to email', 'success')
        else:
            flash('User does not exist! Try again', 'error')
        return redirect(url_for('forgot'))
    return render_template('forgot-password.html')
    