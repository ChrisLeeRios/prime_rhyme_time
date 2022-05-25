# allows our model to talk to the database
from flask_app.config.mysqlconnection import connectToMySQL

# allows us to flash messages onto our HTML pages
from flask import flash , redirect 

# allows us to use global DATABASE variable
from flask_app import DATABASE

# inport REGEX to validate emails
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.pw_hash = data['pw_hash']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def add_user(cls,data):
        query = 'INSERT INTO users (username, email, pw_hash, created_at, updated_at)'
        query +='VALUES (%(username)s,%(email)s,%(pw_hash)s,NOW(),NOW());'
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def get_one(cls,data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0]) 

    @classmethod
    def get_by_email(cls,data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return False
        return cls(result[0])

    @classmethod
    def get_by_username(cls,data):
        query = 'SELECT * FROM users WHERE username = %(username)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        if not result:
            return False
        return cls(result[0])

    @classmethod
    def get_all_users(cls):
        query = 'SELECT * FROM users;'
        result = connectToMySQL(DATABASE).query_db(query)
        # we need a blank list to put our dictionaries into
        users = []
        #we are going to check each row in the table
        for row in result:
            #for every row we return, we want to append the dictionary into the user list
            users.append(cls(row))
        # we are going to send back the list of dictionaries to the controller
        return users


    @staticmethod
    def validate_register(user):
        is_valid = True
        if len(user['username'], ) == 0:
            flash("You must enter a User Name!", 'err.username')
            is_valid = False
        if len(user['email']) == 0:
            flash("You must enter an email!", 'err.email')
            is_valid = False
        if len(user['pw']) == 0:
            flash("You must enter a Password!", 'err.pw')
            is_valid = False
        if len(user['pw1']) == 0 and len(user['pw']) > 7 :
            flash("You must confirm your Password!", 'err.pw1')
            is_valid = False
        if len(user['pw']) < 8 and len(user['pw']) != 0 :
            flash("Password must be atleast 8 characters!", 'err.pw')
            is_valid = False
        if len(user['username']) < 2 and len(user['username']) != 0:
            flash("User Name must be at least 2 characters!", 'err.username')
            is_valid = False
        if not user['pw'] == user["pw1"] and len(user['pw1']) != 0:
            flash("Passwords do not match!", 'err.pw')
            is_valid = False
        if len(user['email']) > 0:
            if not EMAIL_REGEX.match(user["email"]):
                flash("Invalid email address!", 'err.email')
                is_valid = False
        if User.get_by_email(user):
            flash("This email is already in use!", 'err.email')
            is_valid = False
        return is_valid