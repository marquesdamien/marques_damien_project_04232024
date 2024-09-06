from flask_app import app
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import card, deck, user


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
    return redirect('/createdeck')


@app.get('/magiclist')
def magiclist():
    magic_decks = deck.Deck.get_all_magic()
    return render_template('magiclist.html', decks = magic_decks)

@app.get('/yugiohlist')
def yugiohlist():
    yugioh_decks = deck.Deck.get_all_yugioh()
    return render_template('yugiohlist.html', decks=yugioh_decks)

@app.get('/yourdecks')
def yourdecks():
    if "user_id" not in session:
        flash("You must be logged in to access this page")
        return redirect('/')
    user_id = session.get('user_id')
    decks = deck.Deck.get_all_by_userid(user_id)
    return render_template('yourdecks.html', decks=decks)

@app.get('/deck/view/<int:deck_id>')
def view_deck(deck_id):
    if "user_id" not in session:
        flash("You must be logged in to access this page")
        return redirect('/')
    try:
        deck_viewed = deck.Deck.get_one_by_deck_id(deck_id)
        if deck_viewed is None:
            flash("Deck not found")
            return redirect('/yourdecks')
        
        return render_template('viewdeck.html', deck=deck_viewed)
    
    except Exception as e:
        print(f"Error: {e}")
        flash("An error occurred while retrieving the deck")
        return redirect('/yourdecks')


@app.get('/deck/edit/<int:deck_id>')
def update_deck(deck_id):
    if "user_id" not in session:
        flash("You must be logged in to access this page")
        return redirect('/')
    print("in Edit page:" , deck_id)
    deck_viewed = deck.Deck.get_one_by_deck_id(deck_id)
    cards_viewed = deck_viewed.cards
    return render_template('editdeck.html', deck = deck_viewed, cards = cards_viewed)

@app.post('/deck/edit')
def submit_edits():
    if "user_id" not in session:
        flash("You must be logged in to access this page")
        return redirect('/')

    data = {
        'deck_id': request.form['deck_id'],
        'deck_name': request.form['deck_name'],
        'decktype': request.form['decktype'],
        'user_id': request.form['user_id']
    }

    cards_data = []
    card_index = 0
    while f'cards[{card_index}]' in request.form:
        card_data = {
            'deck_id': data['deck_id'],
            'card_name': request.form[f'cards[{card_index}]'],
            'deck_user_id': data['user_id']
        }
        cards_data.append(card_data)
        card_index += 1

    try:
        deck.Deck.remove_cards_by_deck_id(data['deck_id'])

        updated_deck = deck.Deck.update_deck(data)
        
        if updated_deck:
            for card_data in cards_data:
                deck.Deck.add_card_to_deck(card_data)

            return redirect('/yourdecks')
        else:
            flash("Failed to update deck.")
            return redirect(f'/deck/view/{data["deck_id"]}')

    except Exception as e:
        print(f"Error updating deck: {e}")
        flash("There was an issue updating the deck. Please try again.")
    
    return redirect(f'/deck/view/{data["deck_id"]}')







@app.route('/deck/delete/<int:id>')
def delete_deck(id):
    if "user_id" not in session:
        flash("You must be logged in to access this page")
        return redirect('/')
    deck.Deck.delete_deck(id)
    return redirect('/yourdecks')

@app.post('/deck/remove_card')
def remove_card():
    if "user_id" not in session:
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    data = request.get_json()
    card_id = data.get('card_id')

    if not card_id:
        return jsonify({"status": "error", "message": "Card ID is required"}), 400

    success = deck.Deck.remove_card_by_id(card_id)
    
    if success:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": "Failed to remove card"}), 500




