"""
File:  about/views.py
Author:  Kati Kimble
Date: 09-June-2024

File Description:
- Defines the Views for About.
"""

from flask import Blueprint, render_template
from poetry_app.models import AboutMe

# Create a new Blueprint for the 'about' section
about_bp = Blueprint('about', __name__, static_url_path='/about/static', template_folder='templates/about',
                              static_folder='static')

# Define the route for the 'about' page
# This route will handle requests to the '/about' URL
@about_bp.route('/about')
def about():
    # Query the AboutMe table to get the first entry
    about_me_entry = AboutMe.query.first()
    # Extract the content from the entry, or provide a default message if no entry exists
    about_me_content = about_me_entry.content if about_me_entry else "No content available."
    # Render the 'about_me.html' template and pass the content to it
    return render_template('about_me.html', about_me_content=about_me_content)
