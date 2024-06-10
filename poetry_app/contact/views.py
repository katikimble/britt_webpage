'''
File:  contact/views.py
Author:  Kati Kimble
Date: 09-June-2024

File Description:  
- Defines the Views for Contact. 
'''

from flask import redirect, Blueprint, render_template, flash, url_for
from flask_mail import Message
from poetry_app import mail
from poetry_app.contact.forms import ContactForm
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create Contact blueprint
contact_bp = Blueprint('contact', __name__, static_url_path='/contact/static', template_folder='templates/contact',
                              static_folder='static')


# Route for Contact page
@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Process form submission
        name = form.name.data
        email = form.email.data
        message = form.message.data
        britt_wrote_this_email = os.getenv('MAIL_USERNAME')

        # Send email to britt
        britt_message = Message(subject='New Message from Contact Form',
                                sender=email, recipients=[britt_wrote_this_email])
        britt_message.body = f'Name: {name}\nEmail: {email}\nMessage: {message}'
        mail.send(britt_message)

        # Send email to user
        msg_to_user = Message('Thanks for your message!',
                              sender=britt_wrote_this_email,
                              recipients=[email])

        msg_to_user.body = ('This is an automated response to confirm that I have received your message.'
                            '\n\n I will get back to you as soon as possible.\n\n Thank you!\n Brittani Collette x')
        mail.send(msg_to_user)

        # Provide feedback to the user
        success_message = 'Message Received! Thank you.'
        flash(success_message)
        return redirect(url_for('contact.contact'))

    return render_template('contact_pg.html', form=form)