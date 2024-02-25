from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask_app.models.user import User

# ketu krijojme routet per userin

@app.route('/login')
def loginPage():
    if 'user_id' in session:
        return redirect('/')
    return render_template('register_login.html')


@app.route('/register', methods=['POST'])
def register():
    if 'user_id' in session:
        return redirect('/')
    if not User.validate_userRegister(request.form):
        return redirect(request.referrer)
    user= User.get_user_by_email(request.form)
    if user:
        flash('This account already exist!', 'emailRegister')
        return redirect(request.referrer)
    data={
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])  
    }
    session['user_id']=User.create(data)
    return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    if 'user_id' in session:
        return redirect('/')
    if not User.validate_user(request.form):
        return redirect(request.referrer)
    
    user= User.get_user_by_email(request.form)
    if not user:
        flash('This email doesnt exist!', 'emailLogin')
        return redirect(request.referrer)
    
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash('Incorrect password!', 'passwordLogin')
        return redirect(request.referrer)
    
    session['user_id']= user['id']
    return redirect('/')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')





