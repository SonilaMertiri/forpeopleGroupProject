from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

class Message:
    DB = "forpeopleschema"
    
    def __init__(self, data):
            self.id = data['id']
            self.first_name = data['first_name']
            self.last_name = data['last_name']
            self.message = data['message']
            
            self.created_at = data['created_at']
            self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = "INSERT INTO messages (first_name, last_name, email, message) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(message)s);"
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result

        
        
        
    @staticmethod
    def validate_message(message):
        is_valid=True
        if len(message['first_name'])<2:
            flash("First name is required!" ,'nameMessage')
            is_valid=False
        if len(message['last_name'])<2:
            flash("Last name is required!" ,'lastNameMessage')
            is_valid=False
        if not EMAIL_REGEX.match(message['email']):
            flash("Email is incorrect!" ,'emailMessage')
            is_valid=False
        if len(message['message'])<10:
            flash("Provide a valid message!" ,'mesageMessage')
            is_valid=False
        return is_valid
        
            
        
        
            
                  
                  
