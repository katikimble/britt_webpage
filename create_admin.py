"""
File:  create_admin.py
Author:  Kati Kimble
Date: 09-June-2024
File Description: This script initializes a Flask application, loads environment variables, and ensures that an admin
user is present in the application's database. It either updates the existing admin user or creates a new one based on
the environment variables provided.
"""

import os
from poetry_app import create_app, db
from poetry_app.models import User
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = create_app()
bcrypt = Bcrypt(app)

with app.app_context():
    admin_username = os.getenv("ADMIN_USERNAME")
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_username or not admin_email or not admin_password:
        raise ValueError("ADMIN_USERNAME, ADMIN_EMAIL, and ADMIN_PASSWORD must be set in .env")

    admin = User.query.filter_by(email=admin_email).first()

    if admin:
        # Update existing admin user
        admin.username = admin_username
        admin.password_hash = bcrypt.generate_password_hash(admin_password).decode('utf-8')
        print(f"Admin user {admin_username} updated.")
    else:
        # Create a new admin user
        hashed_password = bcrypt.generate_password_hash(admin_password).decode('utf-8')
        admin = User(username=admin_username, email=admin_email, password_hash=hashed_password, is_admin=True)
        db.session.add(admin)
        print(f"Admin user {admin_username} created.")

    db.session.commit()



