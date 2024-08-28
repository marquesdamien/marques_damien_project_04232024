from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import deck, user, comment

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/login_register')
def login_register():
    return render_template('register.html')

@app.post('/users/create')
def create_user():
    if user.User.create_user(request.form):
        return redirect('/')
    return redirect('/')

@app.post('/users/login')
def login():
    if user.User.login(request.form):
        return redirect('/')
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')