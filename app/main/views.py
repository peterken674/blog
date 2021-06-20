from flask import render_template
from . import main


@main.route('/')
def index():

    title='Home | Blogg'


    return render_template('home.html', title=title)