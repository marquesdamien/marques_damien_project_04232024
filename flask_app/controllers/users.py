from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import show, user

@app.route('/')
def home():
    return render_template('Home.html')

@app.post('/users/create')
def create_user():
    if user.User.create_user(request.form):
        return redirect('/Shows_dash')
    return redirect('/')

@app.post('/users/login')
def login():
    if user.User.login(request.form):
        return redirect('/Shows_dash')
    return redirect('/')

@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/')