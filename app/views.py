from flask import render_template
from app import app  # Import the Flask instance we created.

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Cyrus'}  # Mock user.
    posts = [  # Mock array of posts.
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
