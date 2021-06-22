from flask import render_template, url_for
from flask.globals import request
from flask_mail import Message
from flask_wtf import form
from werkzeug.utils import redirect
from . import main
from .forms import NewBlog, NewComment, UpdateProfilePic
from ..models import Post,Comment, User
from .. import db, photos, mail
from flask_login import login_required, current_user
import markdown2
from ..requests import get_quote

@main.route('/')
def index():

    title='Blogg'
    quote = get_quote()

    posts = Post.get_posts()
    formatted_posts = []
    for post in posts:
        post_dict = {'obj': post}
        post_dict['formatted_content'] = markdown2.markdown(post.content,extras=["code-friendly", "fenced-code-blocks"])
        formatted_posts.append(post_dict)

    return render_template('home.html', title=title, formatted_posts=formatted_posts, quote=quote)

@main.route('/new-article', methods = ['GET', 'POST'])
@login_required
def new_article():
    title = "Write blog | Blogg"
    article_form = NewBlog()
    subscribed_users = User.query.filter_by(sub=True).all()

    if current_user in subscribed_users:
        subscribed_users.remove(current_user)


    if article_form.validate_on_submit():
        new_post = Post(title = article_form.title.data, content = article_form.content.data, user=current_user)

        new_post.save_post()

        post = Post.query.filter_by(title=new_post.title).first()

        with mail.connect() as conn:
            sender_email = 'peter.kimani@student.moringaschool.com'
            for user in subscribed_users:
                subject = "New post from " + current_user.fname.capitalize() + " " + current_user.lname.capitalize() + " on Blogg."

                email = Message(recipients=[user.email], sender=sender_email, subject=subject)

                email.body= render_template("email/new_post.txt", poster=current_user, post=post)
                email.html = render_template("email/new_post.html")

            conn.send(email)

        return redirect(url_for('main.index'))


    return render_template('new-article.html', title=title, article_form = article_form)

@main.route('/article/<int:id>', methods = ['GET', 'POST'])
def article(id):

    post = Post.query.filter_by(id=id).first()
    title = post.title
    formatted_post = markdown2.markdown(post.content,extras=["code-friendly", "fenced-code-blocks"])
    form = NewComment()
    comments = Comment.get_comments(id)

    formatted_comments = []
    for comment in comments:
        comment_dict = {'obj': comment}
        comment_dict['formatted_comment'] = markdown2.markdown(comment.comment,extras=["code-friendly", "fenced-code-blocks"])
        formatted_comments.append(comment_dict)

    if form.validate_on_submit():
        new_comment = Comment(comment=form.comment.data, user=current_user, post=post)
        if new_comment.comment:
            new_comment.save_comment()
        return redirect(request.referrer)

    return render_template('article.html', title=title, post=post, formatted_post=formatted_post, form=form, comments=formatted_comments)

@main.route('/user/<int:id>/<username>', methods = ['GET', 'POST'])
def profile(id, username):

    form = UpdateProfilePic()
    user = User.query.filter_by(id=id).first()
    posts = Post.get_posts_by_user(id)

    title = '{} {} | Profile'.format(user.fname, user.lname)

    if form.validate_on_submit():
        filename = photos.save(form.profile.data)
        profile_pic_path = f'img/{filename}'
        user.profile_pic_path = profile_pic_path
        db.session.commit()
        return redirect(url_for('main.profile', id=id, username=user.username))

    return render_template('profile.html', posts=posts, form=form, user=user, title=title)

@main.route('/<int:id>/', methods = ['GET', 'POST'])
@login_required
def like(id):
    post = Post.query.filter_by(id=id).first_or_404()
    current_user.like_post(post)
    db.session.commit()
    return redirect(request.referrer)

@main.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    post = Post.query.filter_by(id=id).first_or_404()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.index'))

@main.route('/article/<int:id>/edit', methods = ['GET', 'POST'])
@login_required
def edit_article(id):
    title = "Edit blog | Blogg"
    article_form = NewBlog()
    post = Post.query.filter_by(id=id).first()

    if request.method == 'GET':
        article_form.title.data = post.title
        article_form.content.data = post.content

    if article_form.validate_on_submit():
        post.title = article_form.title.data
        post.content = article_form.content.data

        db.session.commit()

        return redirect(url_for('main.article', id=id))


    return render_template('new-article.html', title=title, article_form = article_form)

@main.route('/del/<int:id>', methods=['GET', 'POST'])
def del_comment(id):
    comment = Comment.query.filter_by(id=id).first_or_404()
    db.session.delete(comment)
    db.session.commit()
    return redirect(request.referrer)