"""
File:  poems/views.py
Author:  Kati Kimble
Date: 09-June-2024

File Description:
- Defines the Views for Poems.
"""

from flask import Blueprint, render_template
from poetry_app.models import Poem

# Create Poems blueprint
poems_bp = Blueprint('poems', __name__, static_url_path='/poems/static', template_folder='templates/poems',
                              static_folder='static')


# Route for Poems page
@poems_bp.route('/poems')
def poems():
    poetry = Poem.query.order_by(Poem.date_posted.desc()).all()
    return render_template('poems.html', poems=poetry)