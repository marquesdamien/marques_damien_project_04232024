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
        try:
            deck_id = connectToMySQL(cls.db).query_db(query, data)
        except Exception as e:
            flash(f"Error creating deck: {e}")
            return False

        if deck_id:
            card_index = 0
            while f'cards[{card_index}]' in data:
                card_name = data[f'cards[{card_index}]']
                card_data = {
                    "deck_id": deck_id,
                    "card_name": card_name,
                    "deck_user_id": data['user_id']
                }
                cls.add_card_to_deck(card_data)
                card_index += 1
            return cls.get_one_by_deck_id(deck_id)
        return None
    
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM decks
        JOIN users on decks.user_id = users.id;"""

        results = connectToMySQL(cls.db).query_db(query)

        decks = []
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
    def get_all_by_userid(cls, user_id):
        query = """
            SELECT * FROM decks
            JOIN users ON decks.user_id = users.user_id
            WHERE decks.user_id = %(user_id)s
        ;"""
        data = {"user_id": user_id}
        results = connectToMySQL(cls.db).query_db(query, data)
        decks = []
        for result in results:
            deck_data = {
                'deck_id': result['deck_id'],
                'deck_name': result['deck_name'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
                'user_id': result['user_id'],
                'decktype': result['decktype']
            }
            deck_obj = cls(deck_data)
            user_data = {
                'user_id': result['user_id'],
                'first_name': result['first_name'],
                'last_name': result['last_name'],
                'email': result['email'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
                'password': result['password']
            }
            deck_obj.poster = user.User(user_data)
            decks.append(deck_obj)
        return decks
    
    @classmethod
    def get_all_yugioh(cls):
        query = """SELECT * FROM decks
        JOIN users ON decks.user_id = users.user_id
        WHERE decks.decktype = 1;"""
        results = connectToMySQL(cls.db).query_db(query)
        decks = []
        for deck in results:
            deck_obj = Deck(deck)
            user_obj = user.User({
                "user_id" : deck["user_id"],
                "first_name" : deck["first_name"],
                "last_name" : deck["last_name"],
                "email" : deck["email"],
                "created_at" : deck["created_at"],
                "updated_at" : deck.get("updated_at", None),
                "password" : deck["password"]
            })
            deck_obj.poster = user_obj
            deck_obj.cards = deck_obj.get_cards()
            decks.append(deck_obj)
        return decks

    @classmethod
    def get_all_magic(cls):
        query = """SELECT * FROM decks
        JOIN users ON decks.user_id = users.user_id
        WHERE decks.decktype = 0;"""
        results = connectToMySQL(cls.db).query_db(query)
        decks = []
        for deck in results:
            deck_obj = Deck(deck)
            user_obj = user.User({
                "user_id" : deck["user_id"],
                "first_name" : deck["first_name"],
                "last_name" : deck["last_name"],
                "email" : deck["email"],
                "created_at" : deck["created_at"],
                "updated_at" : deck.get("updated_at", None),
                "password" : deck["password"]
            })
            deck_obj.poster = user_obj
            deck_obj.cards = deck_obj.get_cards()
            decks.append(deck_obj)
        return decks
    
    @classmethod
    def validate_deck_data(cls, data):
        is_valid = True 
        if len(data['deck_name']) < 3:
            flash("Deck Name must be at least 3 characters.")
            is_valid = False
        if not data['decktype']:
            flash('Deck Type selection is required')
            is_valid = False
        return is_valid
    
    @classmethod
    def get_one_by_deck_id(cls, deck_id):
        data = {"deck_id": deck_id}
        query = """
            SELECT decks.*, users.first_name, users.last_name, users.email, users.created_at, users.password 
            FROM decks
            JOIN users ON decks.user_id = users.user_id
            WHERE decks.deck_id = %(deck_id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if not result:
            return None
        this_deck = result[0]
        if "deck_id" not in this_deck:
            print(f"Deck ID missing from result: {this_deck}")
            flash("Error: Deck ID missing from result.")
            return None
        deck_obj = Deck({
            'deck_id': this_deck['deck_id'],
            'deck_name': this_deck['deck_name'],
            'created_at': this_deck['created_at'],
            'updated_at': this_deck['updated_at'],
            'user_id': this_deck['user_id'],
            'decktype': this_deck['decktype'],
        })
        user_obj = user.User({
            "user_id": this_deck["user_id"],
            "first_name": this_deck["first_name"],
            "last_name": this_deck["last_name"],
            "email": this_deck["email"],
            "created_at": this_deck["users.created_at"],
            "password": this_deck["password"]
        })
        deck_obj.poster = user_obj
        deck_obj.cards = deck_obj.get_cards()
        return deck_obj
    
    @classmethod
    def update_deck(cls, data):
        if not cls.validate_deck_data(data):
            return False

        query = """
        UPDATE decks
        SET deck_name = %(deck_name)s, decktype = %(decktype)s
        WHERE deck_id = %(deck_id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        
        cls.delete_all_cards_for_deck(data['deck_id'])

        card_index = 0
        while f'cards[{card_index}]' in data:
            card_name = data[f'cards[{card_index}]']
            card_data = {
                "deck_id": data['deck_id'],
                "card_name": card_name,
                "deck_user_id": data['user_id']
            }

            cls.add_card_to_deck(card_data)
            card_index += 1

        updated_deck = cls.get_one_by_deck_id(data['deck_id'])

        return updated_deck






    
    @classmethod
    def delete_deck(cls, deck_id):
        cls.delete_all_cards_for_deck(deck_id)
        query = """
        DELETE FROM decks
        WHERE deck_id = %(deck_id)s
        ;"""
        data = {"deck_id": deck_id}
        connectToMySQL(cls.db).query_db(query, data)
        return
    
    def get_cards(self):
        print(f"Fetching cards for deck ID: {self.deck_id}")
        query = "SELECT * FROM cards WHERE deck_id = %(deck_id)s;"
        data = {"deck_id": self.deck_id}
        cards_data = connectToMySQL(self.db).query_db(query, data)
        print(f"Cards data fetched: {cards_data}")
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
        print(f"Adding card to deck with data: {card_data}")
        query = """
        INSERT INTO cards (deck_id, card_name, deck_user_id) 
        VALUES (%(deck_id)s, %(card_name)s, %(deck_user_id)s)
        ;"""
        try:
            result = connectToMySQL(cls.db).query_db(query, card_data)
            print(f"Insert result: {result}")
            return result
        except Exception as e:
            print(f"Error inserting card: {e}")
            flash("Error inserting card.")
            raise
        
    @classmethod
    def remove_card_by_id(cls, card_id):
        query = """
        DELETE FROM cards 
        WHERE cards_id = %(card_id)s
        ;"""
        data = {"card_id": card_id}
        try:
            connectToMySQL(cls.db).query_db(query, data)
            print(f"Card with ID {card_id} removed.")
        except Exception as e:
            print(f"Error removing card with ID {card_id}: {e}")
            flash(f"Error removing card: {e}")

    @classmethod
    def remove_cards_by_deck_id(cls, deck_id):
        query = "DELETE FROM cards WHERE deck_id = %(deck_id)s;"
        data = {'deck_id': deck_id}
        return connectToMySQL(cls.db).query_db(query, data)
