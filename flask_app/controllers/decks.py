from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import deck, user, comment

@app.route('/magiclist')
def magiclist():
    return render_template('magiclist.html')

@app.route('/yugiohlist')
def yugiohlist():
    return render_template('yugiohlist.html')

@app.route('/yourdecks')
def yourdecks():
    return render_template('yourdecks.html')