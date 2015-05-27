from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm
from .models import User

# Register this with Flask-Login through the decorator.
@lm.user_loader
def load_user(id):
    # User id is unicode string so convert to int.
    return User.query.get(int(id))

# The before_request decorator ensures that this function will run before the view 
# function each time a request is received.
@app.before_request
def before_request():
    # current_user global set by FLask-Login.
    # Assign to flask.g.user object so all requests will have access, even inside 
    # templates.
    g.user = current_user

# Ensure index page is only seen by logged in users.
@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    # Pass in arguments to html template.
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)

# oid.loginhandler decorator to inform FLask-OpenID that this is the login view 
# function.
@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    # If already logged in user, don't re-login.
    # g is a global set up by Flask as a place to store and share data during the 
    # life of a request.
    if g.user is not None and g.user.is_authenticated():
        # Let Flask build the URL by using url_for to obtain the URL for the index
        # view function.
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # Store whether to remember user log-in information in Flask session.
        # flask.session is similar to flask.g, except that data stored in it is 
        # available not only during that request but also through any future 
        # requests made by the same client.
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    # If fields fail validation or user hasn't filled out, render form template.
    return render_template('login.html', 
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

# resp contains information returned by the OpenID provider.
@oid.after_login
def after_login(resp):
    # Need valid email.
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    # Look for the provided email in the DB.
    user = User.query.filter_by(email=resp.email).first()
    # If not found, add as new user.
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    # Load the remember_me value from the Flask session if possible.
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    # Then redirect to either the next page if provided in request or to the index 
    # page. So if user tries to access a page that requires logging in, they'll be 
    # redirected to log in and then, once successful, can return to that page.
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',
                           user=user,
                           posts=posts)
