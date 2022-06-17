import bcrypt
from flask import redirect, render_template, session, flash, request
from flask_app import app
from flask_app.models.user import User
from flask_app.models.post import Post

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def log_and_reg():
    return render_template('log_and_reg.html')

@app.route('/user/register', methods = ['POST'])
def registration():
    if not User.validate_register(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])

    register_data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
        'handle': request.form['handle']
    }

    id = User.register_user(register_data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/user/login', methods = ['POST'])
def login():
    user = User.get_user_by_email(request.form)

    if not user:
        flash('Incorrect Email')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Incorrect Password')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    posts = Post.get_all_posts()
    return render_template('dashboard.html', user = user, all_posts = posts)

@app.route('/user/profile')
def user_profile():
    if 'user_id' not in session:
        return redirect('/')
    user_data = {
        'id': session['user_id']
    }
    post_data = {
        'user_id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    print('A'*50)
    posts = Post.get_posts_by_user(post_data)
    return render_template('my_profile.html', user = user, posts = posts)

@app.route('/user/edit/profile/<int:id>')
def edit_profile(id):
    if 'user_id' not in session:
        return redirect('/logout')
    user_data = {
        'id': session['user_id']
    }
    user = User.get_user_by_id(user_data)
    return render_template('edit_profile.html', user = user)

@app.route('/user/update/profile', methods = ['POST', 'GET'])
def update_profile():
    if 'user_id' not in session:
        return redirect('/logout')
    profile_data = {
        'id' : session['user_id'],
        'first_name' : request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email'],
        'handle' : request.form['handle'],
        'bio' : request.form['bio'],
    }
    User.edit_profile(profile_data)
    return redirect('/user/profile')



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
