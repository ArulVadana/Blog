from flask import Flask,Blueprint,render_template,request,flash,redirect,url_for
from .data import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth=Blueprint("auth",__name__)



@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                login_user(user, remember=True)
                flash('Logged in successfully',category='success')
                return redirect(url_for('view.my_blog'))
            else:
                flash('invalid password',category='error')
        else:
            flash("Email doesn\'t exist!!",category='error')    

    return render_template ('login.html')


@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method=='POST':
        email=request.form.get('email')
        fname=request.form.get('firstName')
        lname=request.form.get('lastName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash ('Email already exist',category='error')
        elif len(email)<4:
            flash('Email must be more than 3 character!',category='error')
        elif len(fname)<2 :
            flash('First name must be more than 1 character!',category='error')
        elif len(lname)<2 :
            flash('Last name must be more than 1 character!',category='error')
        elif password1 != password2:   
            flash('Password doesn\'t match',category='error')
        elif len(password1)<7:
            flash('Password must be more than 6 characters',category='error')

        else:
            new_user=User(email=email,first_name=fname,last_name=lname,password=generate_password_hash(password1,method='sha256'))  
            db.session.add(new_user)
            db.session.commit()  
            login_user(new_user,remember=True)
            flash('Account created Successsfully',category='success')

            return redirect(url_for('view.my_blog',user=current_user))

    return render_template ('signup.html',user=current_user)
     

@auth.route('/logout')
@login_required
def logout():
    logout_user
    return redirect(url_for('view.home'))  
     