"""
File:  subscribe/forms.py
Author:  Kati Kimble
Date: 09-June-2024

File Description:
- - Defines the form for subscribing and unsubscribing for poetry/art updates.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email


class SubscribeForm(FlaskForm):
    """
    SubscribeForm class
    - This form allows users to subscribe or unsubscribe for updates by providing their email address.
    """
    email = StringField('Email:', validators=[DataRequired(), Email()])
    submit_subscribe = SubmitField('Subscribe')
    submit_unsubscribe = SubmitField('Unsubscribe')
