import urllib.request, json

from flask.globals import session
from .models import Quote

base_url=None

def configure_request(app):
    global base_url
    base_url = app.config['QUOTES_API_BASE_URL']
