#database model for our users, database models for our storage content (Waifu pics & categorised by the waifu)

from . import db #from __init__.py package import db = SQLAlchemy()
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin): #this class is inheriting from db.Model & UserMixin
    id = db.Column(db.Integer, primary_key=True) #the id is the primary key, we can have multiple primary key, they become a compound priamry key
    email = db.Column(db.String(120), unique=True, nullable=False)#Nullable=False makes it so that the collumn cannot accept Null values (Must have a value), unique=True means that cannot have duplicate item in column
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    imgs = db.relationship('Img')

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)#id does not need to be initialised, program will increment it auto
    img = db.Column(db.Text, nullable=False, unique=False)
    name = db.Column(db.Text,nullable=False)
    #date = db.Column(db.DateTime(timezone=True),default=func.now())
    mimetype = db.Column(db.Text, nullable=False)#mime type is used to identify type of data, in this case, jpeg, jpg, png ... 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #db.ForiegnKey, enforces that each object needs a user.id associeted to it
    base_data= db.Column(db.BigInteger, nullable=False)
