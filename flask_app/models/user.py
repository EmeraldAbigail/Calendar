from flask_app.config.mysqlconnection import connectToMySQL
import re #the regex module 
from flask_app import app
from flask import flash

# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r'a-zA-Z0-9.+_-')

#User Class 
class User: 
    db ="calendar_schema"
    def __init__(self, data): #data is a dictionary {key: value}
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email= data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    #Create a User
    @classmethod
    def create(cls, data):
        query = """INSERT INTO users
        (first_name, last_name, email, password)
        VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);"""
        user_id = connectToMySQL(cls.db).query_db(query,data)
        return user_id
        
    #Display One User
    @classmethod
    def get_one(cls, id):
        query = "SELECT *FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, {'id': id})
        user = cls(results [0])
        return user
    
    # Create a dictionary with the user's information
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        if not results:
            return []
        user = []
        for User in results:
            User.append(cls(User))
            return User
        
    #Get by specific Email 
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        if not result:
            return None
        return cls(result[0])
    
    #Validation for user form data
    @staticmethod
    def validate_user(user):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        is_valid = True
        #establishing a bool variable to return from function
        #validations and fields to include for first name
        if not user['first_name'].strip():
            is_valid = False
            flash("First Name Required", 'register')
        elif not user['first_name'].isalpha():
            is_valid = False
            flash("First Name should only contain letters", 'register')
        elif len(user['first_name']) < 3:
            flash("First Name must be at least 3 characters.", 'register')
            is_valid = False
        #validations and fields to include for last name
        if not user['last_name'].strip():
            is_valid = False
            flash("Last Name Required", 'register')
        elif not user['last_name'].isalpha():
            is_valid = False
            flash("Last Name should only contain letters", 'register')
        elif len(user['last_name']) < 3:
            flash("Last Name must be at least 3 characters.", 'register')
            is_valid = False
        #validations and fields to include for email
        if not user['email'].strip():
            is_valid = False
            flash("Email Required", 'register')
        if len(user['email']) < 3:
            flash("Email must be a Valid Email", 'register')
            is_valid = False
        # test whether a field matches the pattern
        elif not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email Address!", 'register')
            is_valid = False
        elif User.check_database(user):
            flash("Email already in use", 'register')
            is_valid = False
        #validations and fields to include for password
        if not user["password"].strip():
            is_valid = False
            flash("Password Required", 'register')
        # checks password
        elif len(user['password']) < 8:
            flash("Password must be at least 8 characters.", 'register')
            is_valid = False
        elif user['password'] != user['passConf']:
            is_valid = False
            flash("Passwords must match", 'register')
        return is_valid
    
    #Validate Login
    @staticmethod
    def validate_login(user):
        is_valid = True
        # checks email
        if len(user['email']) < 8:
            flash("Email must be at least 8 characters", 'login')
            is_valid = False
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", 'login')
            is_valid = False
        # checks password
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters", 'login')
            is_valid = False
        return is_valid
    
    #Checks database for emails in use
    @classmethod
    def check_database(cls, data):
        query = """SELECT * FROM users WHERE email= %(email)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    
    #Retrieve unique user
    @classmethod
    def get_by_id(cls, data):
        query = """SELECT * FROM users WHERE id = %(id)s;"""
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

