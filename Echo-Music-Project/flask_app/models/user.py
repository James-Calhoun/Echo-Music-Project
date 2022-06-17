from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

from flask import flash
from flask_app.models.post import Post

class User:
    db = 'echo_music'

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.handle = data['handle']
        self.bio = data['bio']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def register_user(cls, data):
        query = 'INSERT INTO users(first_name, last_name, email, password, handle) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(handle)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    
    @classmethod
    def get_user_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id=%(id)s'
        results = connectToMySQL(cls.db).query_db(query, data)
        user = cls(results[0])
        return user

    @classmethod
    def get_user_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email=%(email)s'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        user = cls(results[0])
        return user
    
    @classmethod
    def edit_profile(cls, data):
        query = 'UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, handle = %(handle)s, bio = %(bio)s, updated_at = NOW() WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)


    # VALIDATIONS

    @staticmethod
    def validate_register(user):
        is_valid = True
        user_in_db = User.get_user_by_email(user)
        if user_in_db:
            flash('Email is associated with another account')
            is_valid = False
        if len(user['first_name']) <= 2:
            flash('First name must be at least 3 characters')
            is_valid = False
        if len(user['last_name']) <= 2:
            flash('Last name must be at least 3 characters')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters long')
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash('Passwords must match')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Please enter valid email address')
            is_valid = False
        if len(user['handle']) < 3:
            flash('Please choose a handle with 3 or more characters')
            is_valid = False

        return is_valid

    @staticmethod
    def validate_login(user):
        is_valid = True
        user_in_db = User.get_user_by_email(user)
        if not user_in_db:
            flash('Email is not associated with an account. Please use Sign Up form to create an account to continue.')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Please enter valid email address')
            is_valid = False
        
        return is_valid