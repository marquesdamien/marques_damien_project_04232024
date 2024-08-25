from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import show, user

@app.route('/')
def home():
    return render_template('home.html')

#CREATE
@app.post('/users/create')
def create_user():
    if user.User.create_user(request.form):
        return redirect('/Shows_dash')
    return redirect('/')
#READ

#UPDATE

#DELETE

@app.post('/users/login')
def login():
    if user.User.login(request.form):
        return redirect('/Shows_dash')
    return redirect('/')

@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/')