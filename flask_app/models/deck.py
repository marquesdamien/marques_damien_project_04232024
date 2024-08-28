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
        if not cls.validate_show_data(data): return False
        query = """
        INSERT INTO decks (deck_name, network, release_date, user_comment, user_id) 
        VALUES (%(show_name)s, %(network)s, %(release_date)s, %(user_comment)s, %(user_id)s )
        ;"""
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM shows
        JOIN users on shows.user_id = users.id;"""
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db).query_db(query)
        # Create an empty list to append our instances of friends
        shows = []
        # Iterate over the db results and create instances of friends with cls.
        for show in results:
            show_obj = Show(show)
            user_obj = user.User({
                "id" : show["users.id"],
                "first_name" : show["first_name"],
                "last_name" : show["last_name"],
                "email" : show["email"],
                "created_at" : show["users.created_at"],
                "updated_at" : show["users.updated_at"],
                "password" : show["password"] 
            })
            show_obj.poster = user_obj
            shows.append(show_obj)
            print(results)
            print(shows)
        return shows
    
    

    @classmethod
    def validate_show_data(cls, data):
        is_valid = True # we assume this is true
        if len(data['show_name']) < 3:
            flash("Title must be at least 3 characters.")
            is_valid = False
        if len(data['network']) < 3:
            flash("Network must be at least 3 characters.")
            is_valid = False
        if not data['release_date']:
            flash('Release date is required')
            is_valid = False
        if len(data['user_comment']) < 3:
            flash('Comments must be at least 3 characters long')
            is_valid = False
        return is_valid
    
    @classmethod
    def get_one_by_show_id(cls, id):
        data = {
            "id" : id
        }
        query = """
            SELECT * FROM shows
            JOIN users ON shows.user_id = users.id
            WHERE shows.id = %(id)s
            ;"""
        
        result = connectToMySQL(cls.db).query_db(query, data)
        this_show = result[0]
        show_obj = Show(this_show)
        user_obj = user.User({
            "id" : this_show["users.id"],
            "first_name" : this_show["first_name"],
            "last_name" : this_show["last_name"],
            "email" : this_show["email"],
            "created_at" : this_show["users.created_at"],
            "updated_at" : this_show["users.updated_at"],
            "password" : this_show["password"] 
        })

        show_obj.poster = user_obj

        return show_obj
    
    @classmethod
    def update_show(cls, data):
        if not cls.validate_show_data(data): 
            return False
        query = """
        UPDATE shows
        SET
            show_name = %(show_name)s,
            network = %(network)s,
            release_date = %(release_date)s,
            user_comment = %(user_comment)s,
            id = %(id)s
        WHERE id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        print(query)
        # data is a dictionary that will be passed into the save method from server.py
        return True
    
    @classmethod
    def delete_show(cls, id):
        data = {
            "id" : id
        }
        query = """
            DELETE FROM shows
            WHERE id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return
    