from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
class Action:
    DB = "forpeopleschema"
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.content = data['content']
        self.image = data['image']
        self.user_id= data['user_id']
        self.event_id= data['event_id']
        self.created_at = data['created_at']
        self.updated_id = data['updated_id']



    @classmethod
    def get_all_actions(cls):
        query= "SELECT * FROM actions;"
        results= connectToMySQL(cls.DB).query_db(query)
        actions=[]
        if results:
            for action in results:
                actions.append(action)
        return actions
    
    @classmethod
    def get_actions_by_event_id(cls, event_id):
        query = "SELECT * FROM actions WHERE event_id = %(event_id)s;"
        data = {'event_id': event_id}
        results = connectToMySQL(cls.DB).query_db(query, data)
        actions = []
        if results:
            for action_data in results:
                action = cls(action_data)
                actions.append(action)
        return actions