"""
File:  admin/forms.py
Author:  Kati Kimble
Date: 09-June-2024

File Description:
- Defines FlaskForm classes using WTForms for handling form validation and rendering.
"""

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class PoemForm(FlaskForm):
    title = StringField('Title:', validators=[DataRequired(), Length(min=2, max=100)])
    content = CKEditorField('Content:', validators=[DataRequired()])
    background = FileField('Upload Background Image: ', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Submit')


class AboutMeForm(FlaskForm):
    content = CKEditorField('Content:', validators=[DataRequired()])
    submit = SubmitField('Submit')


