from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.user import User
from flask import flash


class Event:
    db = "calendar_schema"

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.start_time = data['start_time'] 
        self.end_time = data['end_time']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.location = data['location']
        self.details = data['details']
        self.recurrence = data['recurrence']
        self.reminder = data['reminder']
        self.calendars_id = data['calendars_id']
        self.creator = None  # To store the associated User object

    # Create Event
    @classmethod
    def create_event(cls, data):
        query = """
            INSERT INTO events (title, start_time, end_time, created_at, updated_at, location, details, recurrence, reminder, calendars_id,)
            VALUES (%(title)s, %(start_time)s, %(end_time)s, NOW(), NOW(), %(location)s, %(details)s, %(recurrence)s, %(reminder)s, %(calendars_id)s,)
            """
        event_id = connectToMySQL(cls.db).query_db(query, data)
        return cls(cls.one_event(event_id))

    # Validate Form Data
    @staticmethod
    def is_valid(form_data):
        valid_status = True
        if not form_data['title'].strip():
            valid_status = False
            flash("Please enter an Event.", "event")
        return valid_status

    # READ ONE
    @classmethod
    def one_event(cls, event_id):
        query = """ 
            SELECT *
            FROM events
            WHERE id = %(event_id)s
            """
        data = {'event_id': event_id}
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            return cls(results[0])
        return None

    @classmethod
    def event_details(cls, event_id):
        query = """ 
            SELECT events.*, users.id as user_id, users.first_name, users.last_name, users.email
            FROM events
            JOIN users ON events.users_id = users.id
            WHERE events.id = %(event_id)s 
            """
        data = {'event_id': event_id}
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            event = cls(results[0])
            event.creator = User({
                'id': results[0]['user_id'],
                'first_name': results[0]['first_name'],
                'last_name': results[0]['last_name'],  
                'email': results[0]['email']
            })
            return event
        return None

    # READ ALL
    @classmethod
    def all_event_details(cls):
        query = """ 
            SELECT events.*, users.id as user_id, users.first_name
            FROM users 
            JOIN events ON users.id = events.users_id
            ORDER BY events.id DESC
            """
        results = connectToMySQL(cls.db).query_db(query)
        events = []
        for row in results:
            event = cls(row)
            event.creator = User({'id': row['user_id'], 'first_name': row['first_name']})
            events.append(event)
        return events


    # UPDATE Post Information
    @classmethod
    def update_event(cls, data):
        query = """
            UPDATE events
            SET 
            title = %(title)s,
            start_time = %(start_time)s,
            end_time = %(end_time)s,
            location = %(location)s,
            details = %(details)s,
            recurrence = %(recurrence)s,
            reminder = %(reminder)s
            WHERE id = %(event_id)s;
            """
        return connectToMySQL(cls.db).query_db(query, data)

    # DELETE Post Information 
    @classmethod
    def delete_event(cls, event_id):
        query = """ 
            DELETE FROM events
            WHERE id = %(event_id)s;
            """
        data = {'event_id': event_id}
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def event_check(data):
        form_valid = True
        if len(data['title']) < 4:
            flash('Must be at least 5 characters')
            form_valid = False
        return form_valid

# Event by User
    @classmethod
    def events_by_user(cls, user_id):
        query = """ 
            SELECT events.*, users.id as user_id, users.first_name
            FROM users 
            JOIN events ON users.id = events.users_id
            WHERE users.id = %(user_id)s
            ORDER BY events.id DESC
            """
        data = {'user_id': user_id}
        results = connectToMySQL(cls.db).query_db(query, data)
        events = []
        for row in results:
            event = cls(row)
            event.creator = User({'id': row['user_id'], 'first_name': row['first_name']})
            events.append(event)
        return events

