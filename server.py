from flask_app import app
#here we import our controllers
from flask_app.controllers import  users, events, donations, news, messages

if __name__ == "__main__":
    app.run(debug=True)