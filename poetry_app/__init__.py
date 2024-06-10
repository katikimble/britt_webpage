"""
File:  poetry_app/__init__.py
Author:  Kati Kimble
Date: 09-June-2024

This module initializes and configures a Flask application with various extensions and blueprints.

Key Features:
1. **Environment Variables**: Loads configuration settings from a `.env` file using `dotenv`.
2. **Flask Extensions**: Initializes several Flask extensions for database management, user authentication, password hashing, database migrations, rich text editing, and email support.
3. **Configuration**: Defines a `Config` class to manage application settings, including secret keys, database URIs, CKEditor settings, file upload paths, and email server configurations.
4. **Application Factory**: Implements a `create_app` function to configure and initialize the Flask application, register blueprints for modularity, and set up the application context for extensions.

### Detailed Description of Components:

- **Flask Extensions**:
  - `SQLAlchemy`: ORM for database interactions.
  - `Flask-Bcrypt`: Utility for hashing passwords.
  - `Flask-Login`: Manages user sessions and authentication.
  - `Flask-Migrate`: Handles database migrations using Alembic.
  - `Flask-Mail`: Supports email functionalities.
  - `Flask-CKEditor`: Integrates CKEditor for rich text editing.

- **Configuration Class**:
  - `SECRET_KEY`: Ensures the security of session cookies.
  - `SQLALCHEMY_DATABASE_URI`: Specifies the database connection URI.
  - `CKEDITOR_PKG_TYPE` and `CKEDITOR_HEIGHT`: Configure the CKEditor package and its height.
  - `UPLOAD_FOLDER`: Defines the directory for file uploads.
  - `MAIL_*`: Configures email server settings for sending emails.

- **Application Factory Pattern**:
  - `create_app()`: Sets up the Flask application instance with configuration settings and initializes extensions within
     the app context.
  - Registers multiple blueprints for different parts of the application, promoting modularity and separation of
    concerns.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_ckeditor import CKEditor
import os
from flask_mail import Mail

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'admin.login'
login_manager.login_message_category = 'info'
migrate = Migrate()
mail = Mail()


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI',
                                        'sqlite:///site.db')
    CKEDITOR_PKG_TYPE = 'full'  # Full package of CKEditor
    CKEDITOR_HEIGHT = 400  # Set the height of the editor
    CKEDITOR_FILE_UPLOADER = ''  # Disable file uploader
    UPLOAD_FOLDER = 'poetry_app/static/uploads'
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions with app context
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    ckeditor = CKEditor(app)

    from poetry_app.models import User

    # Register blueprints
    from poetry_app.admin.views import admin
    from poetry_app.main.views import main
    from poetry_app.contact.views import contact_bp
    from poetry_app.about.views import about
    from poetry_app.art.views import art
    from poetry_app.poems.views import poems_bp
    from poetry_app.subscribe.views import subscribe_bp
    from poetry_app.about.views import about_bp

    app.register_blueprint(admin)
    app.register_blueprint(main)
    app.register_blueprint(contact_bp)
    app.register_blueprint(art)
    app.register_blueprint(subscribe_bp)
    app.register_blueprint(poems_bp)
    app.register_blueprint(about_bp)

    return app
