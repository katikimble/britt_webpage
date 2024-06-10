"""
File:  subscribe/views.py
Author:  Kati Kimble
Date: 09-June-2024

File Description:
- Defines the views for the subscription functionality, including subscribing, unsubscribing, and sending update emails.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import redirect, url_for, Blueprint, render_template, current_app, flash
from poetry_app import db
from poetry_app.models import Subscriber
from poetry_app.subscribe.forms import SubscribeForm


# Create the subscribe blueprint
subscribe_bp = Blueprint('subscribe', __name__, static_url_path='/subscribe/static',
                         template_folder='templates/subscribe', static_folder='static')


# Route to handle subscribing and unsubscribing
@subscribe_bp.route('/subscribe', methods=['GET', 'POST'])
def handle_subscribe():
    form = SubscribeForm()
    if form.validate_on_submit():
        email = form.email.data

        if form.submit_subscribe.data:
            # Handle subscription
            if not email:
                flash('Email is required!', 'danger')
                return redirect(url_for('subscribe.handle_subscribe'))

            existing_subscriber = Subscriber.query.filter_by(email=email).first()
            if existing_subscriber:
                flash('Email is already subscribed!', 'warning')
                return redirect(url_for('subscribe.handle_subscribe'))

            new_subscriber = Subscriber(email=email)
            db.session.add(new_subscriber)
            db.session.commit()
            flash('Subscribed successfully!', 'success')

        elif form.submit_unsubscribe.data:
            # Handle unsubscription
            subscriber = Subscriber.query.filter_by(email=email).first()
            if not subscriber:
                flash('Email not found!', 'danger')
                return redirect(url_for('subscribe.handle_subscribe'))

            db.session.delete(subscriber)
            db.session.commit()
            flash('Unsubscribed successfully!', 'success')

        return redirect(url_for('subscribe.handle_subscribe'))

    return render_template('subscribe.html', form=form)


# Function to send update emails to all subscribers
def send_update_email(subject, body):
    subscribers = Subscriber.query.all()
    email_list = [subscriber.email for subscriber in subscribers]

    with current_app.app_context():
        sender_email = current_app.config['MAIL_USERNAME']
        sender_password = current_app.config['MAIL_PASSWORD']
        mail_server = current_app.config['MAIL_SERVER']
        mail_port = current_app.config['MAIL_PORT']
        mail_use_tls = current_app.config['MAIL_USE_TLS']

    # Create email message
    for receiver_email in email_list:
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        message.attach(MIMEText(body, 'plain'))

        try:
            # Send email
            server = smtplib.SMTP(mail_server, mail_port)
            if mail_use_tls:
                server.starttls()
            server.login(sender_email, sender_password)
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            print('Email sent to', receiver_email)
        except Exception as e:
            print('Failed to send email to', receiver_email, 'Error:', str(e))