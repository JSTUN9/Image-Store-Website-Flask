from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app(): #creates and configures flask package application
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Justin' #used to sign session cookies for protection against cookie data tampering
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' #SQLAlchemy database is stored in the website folder
    db.init_app(app)
    
    

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/') # registers the blue prints, and includes what prefixes are needed
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Img #we can't import .something, because we can't do .models.func, so we import all the classes we need

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader #
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME): #if database.db not created, we create it, this is created in same folder as __init__.py
        db.create_all(app=app)
        print('Created Database')