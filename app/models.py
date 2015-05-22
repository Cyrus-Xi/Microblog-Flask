from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    # First argument is the 'many' class, second means can use post.author to get
    # the User instance that wrote the post.
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    # Return True unless User should not be allowed to authenticate.
    def is_authenticated(self):
        return True

    # Return True if User is not inactive (e.g., not banned).
    def is_active(self):
        return True

    # Return True only for fake Users who are not supposed to log in.
    def is_anonymous(self):
        return False

    # Return unique identifier for the User in unicode format.
    def get_id(self):
        try:
            return unicode(self.id)  # Python 2.
        except NameError:
            return str(self.id)  # Python 3.

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
