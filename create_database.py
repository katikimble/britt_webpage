"""
File:  create_database.py
Author:  Kati Kimble
Date: 09-June-2024
File Description: This script initializes a Flask application, creates the necessary database tables based on the
defined models, and confirms the successful creation of these tables by printing a message.
"""

from poetry_app import create_app, db

# Create an instance of the Flask application
app = create_app()

# Create database tables within the app context
with app.app_context():
    db.create_all()  # Creates all the database tables defined by the models
    print("Database tables created.")  # Confirmation message

