from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.message import Message
from flask_bcrypt import Bcrypt
import re
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/register', methods= ['POST'])
def register_user():
    # if User.validate_user(request.form) == False:
    is_valid = User.validate_user(request.form)

    if not is_valid:
        return redirect ('/')

    # pw_hash=bcrypt.generate_password_hash(request.form['password'])
    data= {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form["password"]),
    }

    user_id=User.save_user(data) #it's a good idea to save a piece of data in session about the user--best option is user id
    #logging in the user in action
    if not id:
        flash ("Email already taken")
        return redirect ('/')
    session['user_id']= user_id
    return redirect ('/dashboard')



@app.route('/user/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = {
        "email": request.form['email']
    }
    # user_in_db = User.validate_user(data)
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password,request.form['password']):
    # if we get False after checking the password
        flash("Invalid Password")
        return redirect("/")
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect('/dashboard')



@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect ('/')

    data = {
        'id': session ['user_id']
    }

    user = User.get_one(data)
    messages = Message.get_user_messages(data)
    users = User.get_all_users()
    return render_template('dashboard.html', user=user, messages=messages,users=users)



@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')

