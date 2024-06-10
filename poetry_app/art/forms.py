"""
File:  art/forms.py
Author:  Kati Kimble
Date: 09-June-2024

File Description:
- Defines FlaskForm class using WTForms for handling form validation and rendering.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired


class UploadArtForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired()])
    art_upload = FileField('Upload Art:', validators=[DataRequired()])
    submit = SubmitField('Upload')
