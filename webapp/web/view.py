from flask import Blueprint, render_template, request, flash, jsonify,redirect,url_for
from flask_login import login_required, current_user
from .data import Blog
from .data import User
from . import db
import json

view=Blueprint("view",__name__)


@view.route('/')
def home():
    page=request.args.get('page',1,type=int)
    blogs = Blog.query.order_by(Blog.date.desc()).paginate(page=page,per_page=3)
    user=User.query.all()


    return render_template ('home.html',blogs=blogs,user=user)



@login_required
@view.route('/myblog',methods=['GET','POST'])    
def my_blog():
    if request.method == 'POST':
        title=request.form.get('title')
        note = request.form.get('note')

        if len(note) < 1:
            flash('Blog is too short!', category='error')
        else:
            new_note = Blog(title=title, data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('added!', category='success')
 
    
              
   
    return  render_template("myblog.html", user=current_user)

@login_required
@view.route('/delete/<int:id>')
def delete(id):
    blog_to_delete=Blog.query.filter_by(id=id).first()
    try:
        db.session.delete(blog_to_delete)
        db.session.commit()
        return redirect(request.referrer)
    except:
        return 'Problem in deleting'


@login_required
@view.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    blog_to_edit=Blog.query.filter_by(id=id).first()
    if request.method =='POST':
        title=request.form.get('title')
        note=request.form.get('note')
        blog_to_edit.title=title
        blog_to_edit.data=note     
        db.session.commit()
        return redirect(url_for('view.my_blog'))

    return render_template('edit.html',blog=blog_to_edit,user=current_user)

