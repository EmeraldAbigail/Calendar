from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask_app.models.user import User
from flask_app.models.event import Event
from flask import flash

#Item Class 
class Item:
    db ="calendar_schema"
    def __init__(self, data):
        self.id = data['id']
        self.item_name = data['item_name']
        self.item_complete = data['item_complete']


    #Get All Items 
    @classmethod
    def get_all_items(cls):
        query = """SELECT * FROM items;"""
        results = connectToMySQL(cls.db).query_db(query)
        items = []
        for row in results:
            items.append(row)
        return items 

    #Update Item
    @classmethod
    def update_item(cls, data):
        query = """UPDATE items 
                    SET item_name = %(item_name)s, item_complete = %(item_complete)s 
                    WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db(query, data)

    #Create Item with Validation 
    @classmethod
    def create_item(cls, data):
        if not data['item_name']:  
            flash("Item name cannot be empty!", "item_error")
            return False 
        query = """INSERT INTO items
                (item_name, item_complete)  
                VALUES (%(item_name)s, %(item_complete)s);"""
        id =connectToMySQL(cls.db).query_db(query, data)
        return id

        
    #Delete Item
    @classmethod
    def delete_item(cls, data):
        query = """DELETE FROM items WHERE id = %(id)s;"""
        connectToMySQL(cls.db).query_db(query, data)

