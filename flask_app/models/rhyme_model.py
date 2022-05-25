# allows our model to talk to the database
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User
# allows us to flash messages onto our HTML pages
from flask import flash 

# allows us to use global DATABASE variable instead of typing it in the name
from flask_app import DATABASE

class Rhyme:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.type = data['type']
        self.content = data['content']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_rhymes(cls):
        query = 'SELECT * FROM rhymes;'
        result = connectToMySQL(DATABASE).query_db(query)
        rhymes = []
        for row in result:
            rhymes.append(cls(row))
        return rhymes

    @classmethod
    def add_rhyme(cls,data):
        query = 'INSERT INTO rhymes (title, type, content, user_id, created_at, updated_at)'
        query += 'VALUES (%(title)s,%(type)s,%(content)s,%(user_id)s,NOW(), NOW());'
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def edit_rhyme(cls,data):
        query = 'UPDATE rhymes SET title = %(title)s,type = %(type)s,content = %(content)s,'
        query += 'updated_at = NOW(),created_at = NOW() WHERE id = %(id)s ;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result 

    @classmethod
    def get_one_rhyme(cls,data):
        query = 'SELECT * FROM rhymes WHERE id = %(id)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result 

    @classmethod
    def delete_rhyme(cls, data):
        query = 'DELETE FROM rhymes WHERE id = %(id)s;'
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result


    @classmethod
    def users_rhymes_join(cls):
        query = 'SELECT * FROM rhymes JOIN users on rhymes.user_id = users.id;'
        result = connectToMySQL(DATABASE).query_db(query)
        rhymes = []
        for row in result:
            rhyme = cls(row)
            user_rhyme = {
                'id' : row['users.id'],
                'username' : row['users.id'],
                'email' : row['users.email'],
                'pw_hash' : row['users.pw_hash'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            rhyme.user_id = User(user_rhyme)
            rhymes.append(rhyme)
        return rhymes


    @staticmethod
    def validate_create(user):
        is_valid = True
        if len(user['title']) == 0:
            flash('You Must Enter A Title.', 'err.title')
            is_valid = False
        if len(user['type']) == 0:
            flash('You Must Enter A Type.', 'err.type')
        if len(user['content']) == 0:
            flash('You Must Enter Some Content.', 'err.content')
            is_valid = False
        return is_valid

