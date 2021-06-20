from flask import render_template, url_for
from flask.globals import request
from flask_wtf import form
from werkzeug.utils import redirect
from . import main
from .forms import NewBlog, NewComment
from ..models import Post,Comment
from .. import db
from flask_login import login_required, current_user
import markdown2

@main.route('/')
def index():

    title='Blogg'

    posts = Post.get_posts()
    formatted_posts = []
    for post in posts:
        post_dict = {'obj': post}
        post_dict['formatted_content'] = markdown2.markdown(post.content,extras=["code-friendly", "fenced-code-blocks"])
        formatted_posts.append(post_dict)

    return render_template('home.html', title=title, formatted_posts=formatted_posts)

@main.route('/new-article', methods = ['GET', 'POST'])
@login_required
def new_article():
    title = "Write blog | Blogg"
    article_form = NewBlog()

    if article_form.validate_on_submit():
        new_post = Post(title = article_form.title.data, content = article_form.content.data, user=current_user)
        
        new_post.save_post()

        return redirect(url_for('main.index'))


    return render_template('new-article.html', title=title, article_form = article_form)

@main.route('/article/<id>', methods = ['GET', 'POST'])
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
        new_comment.save_comment()
        return redirect(request.referrer)

    return render_template('article.html', title=title, post=post, formatted_post=formatted_post, form=form, comments=formatted_comments)
