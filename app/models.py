from sqlalchemy.orm import backref
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
from sqlalchemy import desc

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    subscribed = db.Column(db.Boolean)
    password_hash = db.Column(db.String(255))

    posts = db.relationship('Post', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    liked_posts = db.relationship('PostLike', foreign_keys='PitchLike.user_id', backref='user', lazy='dynamic')
    liked_comments = db.relationship('CommentLike', foreign_keys='CommentLike.user_id', backref='user', lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('You cannnot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def like_pitch(self, pitch):
        if not self.has_liked_pitch(pitch):
            like = PostLike(user_id=self.id, pitch_id=pitch.id)
            db.session.add(like)

    def unlike_pitch(self, pitch):
        if self.has_liked_pitch(pitch):
            PostLike.query.filter_by(user_id = self.id, pitch_id = pitch.id).delete()

    def has_liked_pitch(self, pitch):
        return PostLike.query.filter(PostLike.user_id == self.id, PostLike.pitch_id == pitch.id).count() > 0 

    def like_comment(self, comment):
        if not self.has_liked_comment(comment):
            like = CommentLike(user_id=self.id, comment_id=comment.id)
            db.session.add(like)

    def unlike_comment(self, comment):
        if self.has_liked_comment(comment):
            CommentLike.query.filter_by(user_id = self.id, comment_id = comment.id).delete()

    def has_liked_comment(self, comment):
        return CommentLike.query.filter(CommentLike.user_id == self.id, CommentLike.comment_id == comment.id).count() > 0 

    def __repr__(self):
        return f'User {self.username}'

class Quote:
    '''Define the quote response from the API.
    '''
    def __init__(self, id, author, quote):
        self.id = id
        self.author = author
        self.quote = quote

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255))
    content = db.Column(db.String())
    posted = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    likes = db.relationship('PostLike', backref='post', lazy='dynamic')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def save_post(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_posts(cls):
        posts = Post.query.order_by(desc(Post.posted)).all()
        return posts

    @classmethod
    def get_posts_by_user(cls, id):
        posts = Post.query.filter_by(user_id=id).all()
        return posts

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer,primary_key = True)
    comment = db.Column(db.String())
    posted = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    likes = db.relationship('CommentLike', backref='comment', lazy='dynamic')

    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, id):
        comments = Comment.query.filter_by(pitch_id=id)
        return comments



class PostLike(db.Model):
    __tablename__ = "post_likes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

class CommentLike(db.Model):
    __tablename__ = 'comment_likes'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))