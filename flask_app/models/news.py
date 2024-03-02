from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class News:
    DB = "forpeopleschema"
    
    def __init__(self, data):
        self.id = data.get('id')
        self.title = data.get('title')
        self.content = data.get('content')
        self.newsphoto = data.get('newsphoto')
        self.user_id = data.get('user_id')

    @classmethod
    def create(cls, data):
        query = "INSERT INTO news (title, content, newsphoto, user_id) VALUES (%(title)s, %(content)s, %(newsphoto)s, %(user_id)s);"
        try:
            result = connectToMySQL(cls.DB).query_db(query, data)
            return result
        except Exception as e:
            print(f"Error occurred while inserting news article: {e}")
            return None





    

    @classmethod
    def get_all(cls):
        query = "SELECT id, title, content, newsphoto, user_id FROM news;"
        results = connectToMySQL(cls.DB).query_db(query)
        news = []
        if results:
            for new in results:
                news.append(new)
        return news

    #shikoje me kujdes kete ne kete menyre do shtojme donations
    
    @classmethod
    def get_news_by_id(cls, data):
        query = "SELECT * FROM news LEFT JOIN users ON news.user_id = users.id WHERE news.id = %(id)s;"
        result = connectToMySQL(cls.DB).query_db(query, data)
        if result:
            return result[0]  # Return the first row of the result
        return None 

    @classmethod
    def deleteNews(cls,data):
        query="DELETE FROM news WHERE id=%(id)s;"
        return connectToMySQL(cls.DB).query_db(query,data)
    
    @classmethod
    def update(cls,data):
        query="UPDATE news SET title= %(title)s, content= %(content)s, newsphoto=%(newsphoto)s WHERE news.id=%(id)s;"
        return connectToMySQL(cls.DB).query_db(query,data)