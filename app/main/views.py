from flask import render_template
from . import main
from .forms import NewBlog


@main.route('/')
def index():

    title='Home | Blogg'


    return render_template('home.html', title=title)

@main.route('/new-article')
def new_article():
    title = "Write blog | Blogg"
    article_form = NewBlog()

    return render_template('new-article.html', title=title, article_form = article_form)