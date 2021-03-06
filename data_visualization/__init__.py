import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

from config import config

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'forms.login_form'

mail = Mail()

from . import models
from .callbacks import load_user, unauthorized

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from .main_blueprint import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .forms_blueprint import forms as forms_blueprint
    app.register_blueprint(forms_blueprint)

    from .api_blueprint import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app
