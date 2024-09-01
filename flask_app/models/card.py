from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import deck



class Card:
    db = "deckbuildersocials"
    def __init__( self , data ):
        self.cards_id = data['cards_id']
        self.decks_id = data['decks_id']
        self.card_name = data ['card_name']

