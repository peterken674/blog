from flask import render_template, url_for
from werkzeug.utils import redirect
from . import main
from .forms import NewBlog
from ..models import Post
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