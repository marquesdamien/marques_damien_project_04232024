from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import deck, user, comment


@app.get('/createdeck')
def add_deck_page():
    if "user_id" not in session:
        flash("You must be logged in to access this page")
        return redirect('/')
    return render_template('createdeck.html')

@app.post('/deck/create')
def create_deck():
    if "user_id" not in session:
        flash("You must be logged in to access this page")
        return redirect('/')
    if deck.Deck.create_deck(request.form):
        return redirect('/yourdecks')
    is_valid = deck.Deck.validate_deck_data(request.form)
    print("xxxxxxxxxxxxxxxxxxxxx")
    print(request.form)
    print(is_valid)
    return redirect('/yourdecks')


@app.get('/magiclist')
def magiclist():
    return render_template('magiclist.html')

@app.get('/yugiohlist')
def yugiohlist():
    return render_template('yugiohlist.html')

@app.get('/yourdecks')
def yourdecks():
    if "user_id" not in session:
        flash("You must be logged in to access this page")
        return redirect('/')
    return render_template('yourdecks.html')

@app.get('/deck/view/<deck_id>')
def view_deck(deck_id):
    deck_viewed, cards_viewed = deck.Deck.get_one_by_deck_id(deck_id)
    return render_template('viewdeck.html', deck = deck_viewed, cards = cards_viewed)

@app.get('/deck/edit/<deck_id>')
def edit_deck(deck_id):
    if "user_id" not in session:
        flash("You must be logged in to access this page")
        return redirect('/')
    print("in Edit page:" , deck_id)
    deck_viewed, cards_viewed = deck.Deck.get_one_by_deck_id(deck_id)
    return render_template('editdeck.html', deck = deck_viewed, cards = cards_viewed)

@app.post('/deck/edit')
def submit_edits():
    if "user_id" not in session:
        flash("You must be logged in to access this page")
        return redirect('/')
    if deck.Deck.update_deck(request.form):
        return redirect('/yourdecks')
    is_valid = deck.Deck.validate_deck_data(request.form)
    print("xxxxxxxxxxxx")
    print(request.form)
    print(is_valid)
    return redirect(f'/deck/view/{request.form["id"]}')

@app.route('/deck/delete/<int:id>')
def delete_deck(id):
    if "user_id" not in session:
        flash("You must be logged in to access this page")
        return redirect('/')
    deck.Deck.delete_deck(id)
    return redirect('/yourdecks')