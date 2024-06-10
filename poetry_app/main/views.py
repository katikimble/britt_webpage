'''
File:  main/views.py
Author:  Kati Kimble
Date: 09-June-2024

File Description:
- Defines the Views for Main.
'''

from flask import Blueprint, render_template

# Create a new Blueprint for the 'main' section
main = Blueprint('main', __name__, static_folder='/main/static', template_folder='templates/main')


# Define route for the main page '/' and '/index' URLs
@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html')