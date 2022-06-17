from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Post:
    db = 'echo_music'

    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.author = None

    @classmethod
    def save(cls, data):
        query = 'INSERT INTO posts (content, user_id) VALUES (%(content)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all_posts(cls):
        query = 'SELECT * FROM posts LEFT JOIN users on posts.user_id = users.id order by posts.id desc;'
        results = connectToMySQL(cls.db).query_db(query)
        posts = []
        for row in results:
            post = cls(row)
            author_info = {
                "id" : row['id'],
                "first_name" : row['first_name'],
                "last_name" : row['last_name'],
                "email" : row['email'],
                "password" : row['password'],
                "handle" : row['handle'],
                "bio": row['bio'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at']
            }
            author = user.User(author_info)
            post.author = author
            posts.append(post)
        return posts

    @classmethod
    def selected_post(cls, data):
        query = 'SELECT * FROM posts WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_posts_by_user(cls, data):
        query = 'SELECT * from posts where user_id=%(user_id)s order by id desc;'
        results = connectToMySQL(cls.db).query_db(query, data)
        posts = []
        for post in results:
            posts.append(cls(post))
        return posts

    @classmethod
    def delete_post(cls, data):
        query = 'DELETE FROM posts WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def selected_post(cls, data):
        query = 'SELECT * from posts WHERE id = %(id)s;'
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])


    @classmethod
    def update_post(cls, data):
        query = 'UPDATE posts SET content = %(content)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)


    # POST VALIDATIONS
    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['content']) < 1:
            is_valid = False
            flash('Cannot create an empty post. Get creative! Whats on your mind??')
        return is_valid
