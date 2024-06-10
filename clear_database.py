"""
File:  clear_database.py
Author:  Kati Kimble
Date: 09-June-2024
File Description: This script initializes a Flask application and deletes all rows from the User table in the
application's database.
"""

from poetry_app import create_app, db
from poetry_app.models import User

app = create_app()

with app.app_context():
    # Delete all users from the User table
    num_rows_deleted = User.query.delete()
    db.session.commit()
    print(f"Deleted {num_rows_deleted} rows from the User table.")
