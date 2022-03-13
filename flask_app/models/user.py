from flask_app import app
from flask import flash
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.config.mysqlconnection import connectToMySQL

db = "private_wall2"

class User:
    def __init__(self, data):
        self.id = data ['id']
        self.first_name = data ['first_name']
        self.last_name = data ['last_name']
        self.email = data ['email']
        self.password = data ['password']
        self.created_at = data ['created_at']
        self.updated_at = data ['updated_at']

    @classmethod
    def save_user(cls,data):
        query = """ INSERT into users (first_name, last_name, email, password)
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"""
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all_users(cls):
        query = 'SELECT * FROM users;'
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results= connectToMySQL(db).query_db(query, data)
        #if it doesn't find a matching user
        if len (results) < 1:
            return False
        return cls(results[0])


    @staticmethod
    def validate_user(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid= True
        if len(data['first_name']) < 2:
            flash ("First name has to be longer than 2 characters.")
            is_valid = False
        if len(data['last_name']) < 2:
            flash ('Last Name has to be longer than 2 characters')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Please enter a valid email.')
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) > 0:
            flash ('User another email')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters')
            is_valid = False
        if data ['password'] != data['confirm_password']:
            flash ('Password and confirm password do not match')
            is_valid= False
        return is_valid

