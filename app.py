"""
File:  app.py
Author:  Kati Kimble
Date: 09-June-2024
File Description: This script initializes and runs a Flask web application for the poetry application project.
"""

from poetry_app import create_app

# Create an instance of the Flask application using the factory function
app = create_app()

# Run the Flask development server when this script is executed
if __name__ == '__main__':
    # Start the server in debug mode to enable live reload and detailed error messages
    app.run(debug=True)
