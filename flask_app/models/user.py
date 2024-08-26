from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session

import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class User:
    db = "deckbuildersocials"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.password = data['password']
        self.shows = []

    @classmethod
    def validate_user_data(cls, data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True # we assume this is true
        if len(data['first_name']) < 2:
            flash("First Name must be at least 2 characters.")
            is_valid = False
        if len(data['last_name']) < 2:
            flash("Last Name must be at least 2 characters.")
            is_valid = False
        if len(data['password']) < 8:
            flash('Your Password must be at least 8 characters long.')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Password and Confirm Password do not match.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Please use a valid email address.")
            is_valid = False
        if cls.get_user_by_email(data['email']):
            flash("This email address already has an account.")
            is_valid = False
        return is_valid
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in users:
            users.append(cls(user))
            print(results)
            print(users)
        return users
    
    @classmethod
    def create_user(cls, user_data):
        if not cls.validate_user_data(user_data): return False
        user_data = user_data.copy()
        user_data['password'] = bcrypt.generate_password_hash(user_data['password'])
        
        query = """
        INSERT INTO users (first_name, last_name, email, created_at, updated_at, password) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW(), %(password)s)
        ;"""
        user_id = connectToMySQL(cls.db).query_db(query, user_data)
        session['user_id'] = user_id
        session['user_name'] = f'{user_data["first_name"]} {user_data["last_name"]}'
        return user_id

    @classmethod
    def get_user_by_email(cls, email):
        data = {'email' : email }
        query = """
            SELECT *
            FROM users
            WHERE email = %(email)s
            """
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            return(cls(result[0]))
        return False
    
    @classmethod
    def login(cls, data):
        this_user = cls.get_user_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                session['user_name'] = f'{this_user.first_name} {this_user.last_name}'
                return True
        flash('Your login information was incorrect')
        return False
    
    @classmethod
    def get_user_by_id(cls, id):
        data = {'id' : id }
        query = """
            SELECT *
            FROM users
            WHERE id = %(id)s
            """
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            return(cls(result[0]))
        return False