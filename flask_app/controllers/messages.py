from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.message import Message
from flask import render_template, redirect, request, session, flash
from flask_app import app



@app.route('/contact')
def contact():
    return render_template('contact.html')


# Define sentmessage route
@app.route('/sentmessage', methods=['POST'])
def sent_message():
    if not Message.validate_message(request.form):
        return redirect(request.referrer)
    data={
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'message': request.form['message']  
        }
    Message.create(data)
    return redirect(request.referrer)

    
