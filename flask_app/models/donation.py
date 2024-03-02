from flask_app.config.mysqlconnection import connectToMySQL


class Donation:
    DB = "forpeopleschema"
    def __init__(self, data):
        self.id = data['id']
        self.type = data['type']
        self.user_id = data['user_id']
        self.event_id = data['event_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM donations;"
        results = connectToMySQL(cls.DB).query_db(query)
        donations = []
        if results:
            for row in results:
                donations.append(cls(row))
        return donations

    # Implement other CRUD operations as needed
