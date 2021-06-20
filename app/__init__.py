from flask import Flask
from config import config_options
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)

    #Creating the app configurations
    app.config.from_object(config_options[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Flask extensions
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Setting config
    from .requests import configure_request
    configure_request(app)

    # Registering the blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix ='/auth')

    return app