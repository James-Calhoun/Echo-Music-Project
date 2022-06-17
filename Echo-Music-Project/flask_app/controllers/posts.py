from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.post import Post

@app.route('/post/new')
def add_post():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    return render_template('new_post.html', user = user)

@app.route('/post/new/submit', methods = ['POST'])
def submit_post():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Post.validate_post(request.form):
        return redirect('/post/new')
    post_data = {
        'content': request.form['content'], 
        'user_id': session['user_id']
    }
    Post.save(post_data)
    return redirect('/dashboard')

@app.route('/post/delete/<int:id>')
def delete_listing(id):
    if 'user_id' not in session:
        return redirect('/logout')
    post_data = {
        'id': id
    }
    Post.delete_post(post_data)
    return redirect('/dashboard')

@app.route('/post/edit/<int:id>')
def edit_post(id):
    if 'user_id' not in session:
        return redirect('/logout')
    post_data = {
        'id': id
    }
    post = Post.selected_post(post_data)
    return render_template('edit_post.html', post = post)

@app.route('/update/post/', methods = ['POST'])
def update_post():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Post.validate_post(request.form):
        return redirect('/dashboard')
    post_data = {
        'id' : request.form['id'],
        'content' : request.form['content'],
    }
    print("A"*50)
    print('id is' + request.form['id'])
    Post.update_post(post_data)
    return redirect('/dashboard')
    

