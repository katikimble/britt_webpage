"""
File:  art/views.py
Author:  Kati Kimble
Date: 09-June-2024

File Description:
- Defines the Views for Art.
"""

from flask import Blueprint, render_template
from poetry_app.models import Art

# Create a new Blueprint for the 'art' section
art = Blueprint('art', __name__, static_url_path='/art/static', template_folder='templates/art',
                              static_folder='static')


# Define the route for the 'art_gallery' page
# This route will handle requests to the '/art_gallery' URL
@art.route('/art_gallery')
def art_gallery():
    arts = Art.query.order_by(Art.date_posted.desc()).all()
    return render_template('art.html', arts=arts)


# This route will handle requests to the '/art_detail' URL
@art.route('/art/<int:art_id>')
def art_detail(art_id):
    art_work = Art.query.get_or_404(art_id)
    return render_template('art_detail.html', art=art_work)