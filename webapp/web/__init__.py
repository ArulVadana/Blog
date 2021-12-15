from flask import Flask,Blueprint
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME='user.db'

def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY']='hgyfhgvkuyhiuyh'
    app.config['SQLALCHEMY_DATABASE_URI']=f'sqlite:///{DB_NAME}'
    db.init_app(app)
  


    from .view import view
    from .auth import auth 

    from .data import User,Blog

    create_database(app)


    app.register_blueprint(view,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))


    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
