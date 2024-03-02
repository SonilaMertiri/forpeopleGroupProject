from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Event:
    DB = "forpeopleschema"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.user_id = data['user_id']
        self.image_path = data['image_path']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO events (name, description, user_id, image_path) VALUES (%(name)s, %(description)s, %(user_id)s, %(image_path)s);"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT id, name, description, user_id, image_path, created_at, updated_at FROM events;"
        results = connectToMySQL(cls.DB).query_db(query)
        events = []
        if results:
            for event in results:
                events.append(event)
        return events

    @classmethod
    def get_event_by_id(cls, data):
        query = "SELECT * FROM events LEFT JOIN users ON events.user_id = users.id WHERE events.id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            actions = []
            query2 = "SELECT * FROM actions LEFT JOIN users ON actions.user_id = users.id WHERE actions.event_id = %(id)s;"
            result2 = connectToMySQL(cls.DB).query_db(query2, data)
            if result2:
                for action in result2:
                    actions.append(action)
            result[0]['actions'] = actions
            return result[0]
        return None

    @classmethod
    def deleteEvent(cls, data):
        query = "DELETE FROM events WHERE id=%(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE events SET name= %(name)s, description= %(description)s WHERE events.id=%(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)


    @staticmethod
    def validate_event(event):
        is_valid= True
        if len(event['name'])<2:
            flash('Name should be more than two characters', 'nameEvent')
            is_valid=False
        if len(event['description'])<10:
            flash('Description should be more than 10 characters', 'descriptionEvent')
            is_valid=False
        return is_valid
    
    @staticmethod
    def validate_event_update(event):
        is_valid= True
        if len(event['name'])<2:
            flash('Name should be more than two characters', 'nameEvent')
            is_valid=False
        if len(event['description'])<10:
            flash('Description should be more than 10 characters', 'descriptionEvent')
            is_valid=False
        return is_valid
    
    
    
    
    
    #ACTIONS
    
    # per actions metodaaaaaaaaaaaaat
    @classmethod
    def create_action(cls, data):
        query = "INSERT INTO actions (title, content, image, event_id, user_id) VALUES (%(title)s, %(content)s, %(image)s,  %(event_id)s, %(user_id)s);"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def get_action_by_id(cls, data):
        query = "SELECT * FROM actions WHERE actions.id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            return result[0]  # Return the first row of the result
        return False
    
    @classmethod
    def update_action(cls, data):
        query = "UPDATE actions SET title = %(title)s, content = %(content)s, image = %(image)s WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)
    
    @classmethod
    def delete_action(cls, data):
        query = "DELETE FROM actions WHERE id = %(id)s;"
        return connectToMySQL(cls.DB).query_db(query, data)