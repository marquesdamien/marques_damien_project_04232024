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
        INSERT INTO decks (deck_name, network, release_date, user_comment, user_id) 
        VALUES (%(show_name)s, %(network)s, %(release_date)s, %(user_comment)s, %(user_id)s )
        ;"""
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

        return deck_obj
    
    @classmethod
    def update_deck(cls, data):
        if not cls.validate_deck_data(data): 
            return False
        query = """
        UPDATE decks
        SET
            deck_name = %(deck_name)s,
            decktype = %(decktype)s,
            id = %(id)s
        WHERE id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        print(query)
        # data is a dictionary that will be passed into the save method from server.py
        return True
    
    @classmethod
    def delete_deck(cls, deck_id):
        data = {
            "deck_id" : deck_id
        }
        query = """
            DELETE FROM decks
            WHERE deck_id = %(deck_id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return
    