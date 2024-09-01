from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user, card



class Deck:
    db = "deckbuildersocials"
    def __init__( self , data ):
        self.deck_id = data['deck_id']
        self.deck_name = data['deck_name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.decktype = data['decktype']
        self.cards = self.get_cards()
        self.poster = None


    @classmethod
    def create_deck(cls, data):
        if not cls.validate_deck_data(data): return False
        query = """
        INSERT INTO decks (deck_name, decktype, user_id) 
        VALUES (%(deck_name)s, %(decktype)s, %(user_id)s)
        ;"""
        deck_id = connectToMySQL(cls.db).query_db(query, data)

        if deck_id:
            card_index = 0
            while f'cards[{card_index}]' in data:
                card_name = data[f'cards[{card_index}]']
                card_data = {
                    "deck_id": deck_id,
                    "card_name": card_name
                }
                cls.add_card_to_deck(card_data)
                card_index += 1
            return cls.get_one_by_deck_id(deck_id)
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM decks
        JOIN users on decks.user_id = users.id;"""
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db).query_db(query)
        # Create an empty list to append our instances of friends
        decks = []
        # Iterate over the db results and create instances of friends with cls.
        for deck in results:
            deck_obj = Deck(deck)
            user_obj = user.User({
                "user_id" : deck["users.user_id"],
                "first_name" : deck["first_name"],
                "last_name" : deck["last_name"],
                "email" : deck["email"],
                "created_at" : deck["users.created_at"],
                "updated_at" : deck["users.updated_at"],
                "password" : deck["password"] 
            })
            deck_obj.poster = user_obj
            decks.append(deck_obj)
            print(results)
            print(decks)
        return decks
    
    

    @classmethod
    def validate_deck_data(cls, data):
        is_valid = True # we assume this is true
        if len(data['deck_name']) < 3:
            flash("Title must be at least 3 characters.")
            is_valid = False
        if not data['decktype']:
            flash('Deck Type selection is required')
            is_valid = False
        return is_valid
    
    @classmethod
    def get_one_by_deck_id(cls, deck_id):
        data = {
            "deck_id" : deck_id
        }
        query = """
            SELECT * FROM decks
            JOIN users ON decks.user_id = users.id
            WHERE decks.id = %(id)s
            ;"""
        
        result = connectToMySQL(cls.db).query_db(query, data)
        if not result:
            return None
        
        this_deck = result[0]
        deck_obj = Deck(this_deck)

        user_obj = user.User({
            "user_id" : this_deck["users.user_id"],
            "first_name" : this_deck["first_name"],
            "last_name" : this_deck["last_name"],
            "email" : this_deck["email"],
            "created_at" : this_deck["users.created_at"],
            "updated_at" : this_deck["users.updated_at"],
            "password" : this_deck["password"] 
        })

        deck_obj.poster = user_obj
        deck_obj.cards = deck_obj.get_cards()

        return deck_obj
    
    @classmethod
    def update_deck(cls, data):
        if not cls.validate_deck_data(data): 
            return False
    
        # Update the deck details
        query = """
        UPDATE decks
        SET deck_name = %(deck_name)s, decktype = %(decktype)s, ...
        WHERE id = %(deck_id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
    
        # Clear existing cards for this deck
        cls.delete_all_cards_for_deck(data['deck_id'])
    
        # Insert the new set of cards
        card_index = 0
        while f'cards[{card_index}]' in data:
            card_name = data[f'cards[{card_index}]']
            card_data = {
                "deck_id": data['deck_id'],
                "card_name": card_name
            }
        cls.add_card_to_deck(card_data)
        card_index += 1
    
        return cls.get_one_by_deck_id(data['deck_id'])

    
    @classmethod
    def delete_deck(cls, deck_id):
    # First, delete all cards associated with this deck
        cls.delete_all_cards_for_deck(deck_id)
    
    # Then, delete the deck itself
        query = """
        DELETE FROM decks
        WHERE id = %(deck_id)s
        ;"""
        data = {"deck_id": deck_id}
        connectToMySQL(cls.db).query_db(query, data)
        return
    
    @classmethod
    def get_cards(self):
        query = "SELECT * FROM cards WHERE deck_id = %(deck_id)s;"
        data = {"deck_id": self.deck_id}
        cards_data = connectToMySQL(self.db).query_db(query, data)
        cards = [card.Card(card_info) for card_info in cards_data]
        return cards
    
    @classmethod
    def delete_all_cards_for_deck(cls, deck_id):
        query = """
        DELETE FROM cards WHERE deck_id = %(deck_id)s
        ;"""
        data = {"deck_id": deck_id}
        connectToMySQL(cls.db).query_db(query, data)

    
    @classmethod
    def add_card_to_deck(cls, card_data):
        query = """
        INSERT INTO cards (deck_id, card_name) 
        VALUES (%(deck_id)s, %(card_name)s)
        ;"""
        return connectToMySQL(cls.db).query_db(query, card_data)