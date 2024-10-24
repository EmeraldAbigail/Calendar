from flask import render_template, redirect, flash, request, session
from flask_app.models.user import User
from flask_app.models.event import Event
import datetime

from flask_app import app

#Initialize Bcrypt for password hashing
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

#Route for submitting the user login form
@app.route("/user/login", methods=['POST'])
def login():
    #Retrieve the user from the database based on the provided email 
    user = User.get_by_email(request.form)
    if not User.validate_login(request.form):
        #Redirect the user back to the login/registration form
        flash ("Invalid Email/Password")
        return redirect('/')    
    #Check if the user exists and the password is valid
    if not user or not bcrypt.check_password_hash(user.password, request.form ['password']):
        #Flash an error message if the email/password is invalid
        flash("Invalid Email/Password")
        #Redirect the user back to the login/registration form
        return redirect('/')
    #Store User's ID and First Name in Session
    session['user_id'] = user.id
    session['first_name'] = user.first_name
    #Redirect the user to the calendar
    return redirect('/main')  

#Route for the Calendar
@app.route('/main')
@app.route("/main/<date>")
def main(date = None):
    #Check if the user is logged in 
    if 'user_id' not in session:
        #If the user is not logged in, redirect to the logout route
        return redirect('/')
    if date is None: 
        date_str = datetime.date.today().strftime('%Y-%m-%d')
    else: 
        date_str = date
    data = {
        'date': date_str,
        'users_id': session['user_id']
    } 
    print(data)
    events= Event.events_by_date(data)
    print (events)
    #Render the calendar template with the user's data
    return render_template("main.html", events=events)

#Route for logging out the User
@app.route("/logout")
def logout():
    #Clear the User's session data
    session.clear()
    #Redirect the User to the login/registration page 
    return redirect('/')
