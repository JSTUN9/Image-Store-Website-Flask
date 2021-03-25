# store all the routes of the webserver
from . import db
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
# hashing function, is a function with no inverse, so given password is x, result from function is y, we can obtain y with x using hashing function, but not x with y

#define that this file is the blueprint of our webserver (stores all the url of our webserver)

auth = Blueprint('auth', __name__) # parameters needed for Blueprint object, blueprint_name & import_name

@auth.route('/signup/', methods=['GET', 'POST']) 
def signup():
    if request.method == 'POST':
        email = request.form.get('email') #getting the object with unique id email
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        firstName = request.form.get('firstName')
        print(email)

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists', category='error')

        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(firstName) < 2:
            flash('First Name must be greater than 2 characters', category='error')
        elif len(password1) < 4:
            flash('password must be greater than 4 characters.', category='error')
        elif password1 != password2:
            flash('Password must be same.', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(password1, method='sha256'), first_name=firstName)
            db.session.add(new_user)
            db.session.commit()

            flash('Account creation success.', category='success')
            login_user(new_user, remember=True) #remembers that user is logged in
            
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)#we are passing in anonymos user


@auth.route('/logout/') 
@login_required #we can't logout, if no user is logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/login/', methods=['GET', 'POST'])  # by default this route can only accept GET request, now we add a list of type of requests we can allow.
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user: #if user exists
            if check_password_hash(user.password, password):
                flash ('log in sucessful', category='success')
                login_user(user, remember=True) #remembers that user is logged in
                return redirect(url_for('views.home'))
            else:
                flash ('Incorrect password, try again', category= 'error')
        else:
            flash('User does not exist', category='error')        

    return render_template("login.html", user=current_user)