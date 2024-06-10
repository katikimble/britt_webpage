'''
File:  contact/forms.py
Authors:  Kati Kimble
Date: 09-June-2024

File Description:  
- Defines the Contact form. 
'''

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField


# Define ContactForm
class ContactForm(FlaskForm):
    name = StringField('Name:')
    email = StringField('Email:')
    message = TextAreaField('Message:')
    submit = SubmitField('Submit')