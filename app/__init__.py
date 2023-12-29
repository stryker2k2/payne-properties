from flask import Flask
from wtforms.widgets import TextArea
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_ckeditor import CKEditor
from app.config import Config

import uuid as uuid


# Create a Flask Instance
app = Flask(__name__)

# Parse Config
app.config.from_object(Config)
app.app_context().push()

# Add CKEditor
ckeditor = CKEditor(app)

# Initialize & Migrate Database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Flask Login Setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app import routes

# def create_app(config_class=Config):
    # See https://youtu.be/Wfx4YBzg16s 
