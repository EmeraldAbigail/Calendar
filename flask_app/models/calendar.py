from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
import calendar
from flask_app.models.user import User
from flask_app.models.event import Event
from flask import flash


#Model the class after the Idea table from database
class Calendar:
    db = "calendar_schema"
    def __init__(self,data):
        self.id = data['id']
        self.calendar_id =['calendar_id']
        self.name = data['name']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users = data ['users_id']
        self.calendar = []
    
    #Create Calendar
    @classmethod
    def create(cls, data):
        query = """
            INSERT INTO calendars (calendar_id, name, description,  created_at, updated_at, users_id)
            VALUES (%(calendar_id)s, %(name)s, %(description)s, NOW(), NOW(), %(user_id)s)
            """
        calendar_id = connectToMySQL(cls.db).query_db(query,data)
        print(calendar_id)
        return cls(cls.one_calendar(calendar_id))
    
    
    #Validate Form Data
    @staticmethod
    def is_valid(form_data):
        valid_status = True
        #Save Calendar 
        if not form_data['name'].strip():
            valid_status = False
            flash("Please name the Calendar.", "name")
        
        return valid_status
        
    # READ ONE
    @classmethod
    def one_calendar(cls,users_id):
        query = """ 
                SELECT *
                FROM calendars
                WHERE id = %(calendar_id)s
                """
        data = {'calendar_id': users_id}
        results = connectToMySQL(cls.db).query_db(query,data)
        return results[0]

    @classmethod
    def calendar_details(cls,calendar_id):
        query = """ 
                SELECT *
                FROM users
                LEFT JOIN calendars ON users.user_id = calendars.users_id
                WHERE calendars.calendars_id = %(calendar_id)s 
                """
        data = {'calendar_id': calendar_id}
        results = connectToMySQL(cls.db).query_db(query,data)
        calendar_data = cls(results[0])
        for calendar in results:
            calendar_details = {
                'name': calendar['name'],
                'users_id': calendar['users_id'],
            }
            calendar_data.calendar.append(User(calendar_details))
        return calendar_details
    
    #READ ALL
    @classmethod
    def all_calendar_details(cls):
        query = """ 
                SELECT calendars.*, users.id as user_id, users.first_name
                FROM users 
                JOIN calendars ON users.id = calendars.users_id
                ORDER BY calendars.calendar_id DESC
                """
        results = connectToMySQL(cls.db).query_db(query)
        return results
    
    # UPDATE Calendar Information
    @classmethod
    def update_calendar(cls,data):
        query = """
                UPDATE calendars
                SET 
                name = %(name)s
                description = %(description)s
                WHERE id = %(calendar_id)s;
                """
        results = connectToMySQL(cls.db).query_db(query,data)
        return results
    
    # DELETE Calendar Information 
    @classmethod
    def delete_calendar(cls, calendar_id):
        query = """ 
                DELETE FROM calendars
                WHERE id = %(calendars_id)s;
                """
        data = {'calendars_id': calendar_id}
        results = connectToMySQL(cls.db).query_db(query,data)
        return results
    
    #Check Calendar Name 
    @staticmethod
    def calendar_check(data):
        form_valid = True
        if len(data['name']) < 4:
            flash('Must be at least 5 characters')
            form_valid = False
        
        return form_valid
    
#Calendar by User
    @classmethod
    def calendars_by_user(cls,user_id):
        query = """ 
                SELECT calendars.*, users.id as user_id, users.first_name
                FROM users 
                JOIN calendars ON users.id = calendars.users_id
                WHERE users.id = %(user_id)s
                ORDER BY calendars.calendars_id DESC
                """
        data = {'user_id': user_id}
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    


