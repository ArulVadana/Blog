from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask import Blueprint

import datetime




class Blog(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(1000))
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True),default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    notes = db.relationship('Blog')    





