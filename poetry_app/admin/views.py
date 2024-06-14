"""
File:  admin/views.py
Author:  Kati Kimble
Date: 09-June-2024

File Description:
- Defines the Views for Admin.
"""

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from poetry_app import db, bcrypt
from poetry_app.art.forms import UploadArtForm
from poetry_app.models import User, Poem, AboutMe, Art, Subscriber
from poetry_app.admin.forms import LoginForm, PoemForm, AboutMeForm
from werkzeug.utils import secure_filename
import os
from poetry_app.subscribe.views import send_update_email

# Create the admin blueprint
admin = Blueprint('admin', __name__, static_folder='static', static_url_path='/admin/static',
                  template_folder='templates/admin')


# Function to save uploaded images
def save_image(image):
    filename = secure_filename(image.filename)
    image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    image.save(image_path)
    return filename


# Login route
@admin.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        # Validate user credentials
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data) and user.is_admin:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password!', 'danger')
    return render_template('login.html', title='Login', form=form)


# Dashboard route
@admin.route('/dashboard')
@login_required
def dashboard():
    # Redirect non-admin users to the main page
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
    # Get all poems, about me content, and arts
    poems = Poem.query.filter_by(user_id=current_user.id).all()
    about = AboutMe.query.first()
    arts = Art.query.order_by(Art.date_posted.desc()).all()

    # Fetch all subscribers
    subscribers = Subscriber.query.all()
    num_subscribers = len(subscribers)
    return render_template('dashboard.html', title='Dashboard', poems=poems, about_me=about, arts=arts, subscribers=subscribers, num_subscribers=num_subscribers)


# Route to handle updating about me section
@admin.route('/about', methods=['POST'])
@login_required
def about_me():
    # Redirect non-admin users to the main page
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
    form = AboutMeForm()
    if form.validate_on_submit():
        about = AboutMe.query.first()
        if not about:
            about = AboutMe(content=form.content.data)
            db.session.add(about)
        else:
            about.content = form.content.data
        db.session.commit()
        flash('Your "About Me" content has been updated!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('dashboard.html', title='Dashboard', form=form)


# Route to create new about me section
@admin.route('/about_me/new', methods=['GET', 'POST'])
@login_required
def create_about_me():
    # Redirect non-admin users to the main page
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
    form = AboutMeForm()
    if form.validate_on_submit():
        about = AboutMe(content=form.content.data)
        db.session.add(about)
        db.session.commit()
        flash('About Me section has been created!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('create_about_me.html', title='Create About Me', form=form)


# Route to edit existing about me section
@admin.route('/about_me/<int:about_me_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_about_me(about_me_id):
    # Redirect non-admin users to the main page
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
    about = AboutMe.query.get_or_404(about_me_id)
    form = AboutMeForm()
    if form.validate_on_submit():
        about.content = form.content.data
        db.session.commit()
        flash('About Me section has been updated!', 'success')
        return redirect(url_for('admin.dashboard'))
    elif request.method == 'GET':
        form.content.data = about.content
    return render_template('create_about_me.html', title='Edit About Me', form=form)


# Logout route
@admin.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.login'))


# Route to create new poem
@admin.route('/poem/new', methods=['GET', 'POST'])
@login_required
def new_poem():
    # Redirect non-admin users to the main page
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
    form = PoemForm()
    if form.validate_on_submit():
        background = None
        if form.background.data:
            background = save_image(form.background.data)
        poem = Poem(title=form.title.data, content=form.content.data, user_id=current_user.id,
                    background=background)
        db.session.add(poem)
        db.session.commit()
        # Notify subscribers
        subject = "New Poem Added"
        body = """Hello, 

I just added a new Poem to my collection.  Come check it out!
https://brittaniwrotethis.pythonanywhere.com/poems

If you wish to unsubscribe at any time, please click the link below:
https://brittaniwrotethis.pythonanywhere.com/subscribe, enter your email and click unsubscribe.

Thank you for your support!

Best regards,
Brittani Collette x
        """

        send_update_email(subject, body)
        flash('Your poem has been created and your subscribers were notified!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('create_poem.html', title='New Poem', form=form, legend='New Poem', poem=None)


# Route to update existing poem
@admin.route('/poem/<int:poem_id>/update', methods=['GET', 'POST'])
@login_required
def update_poem(poem_id):
    poem = Poem.query.get_or_404(poem_id)
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
    form = PoemForm()
    if form.validate_on_submit():
        if form.background.data:
            # Save the new background image
            new_background = save_image(form.background.data)
            # Check if the old background is used by other poems or arts
            if poem.background:
                other_poems_using_image = Poem.query.filter(Poem.id != poem.id, Poem.background == poem.background).count()
                arts_using_image = Art.query.filter_by(art_upload=poem.background).count()
                if other_poems_using_image == 0 and arts_using_image == 0:
                    # Remove the old background file from the server
                    old_background_path = os.path.join(current_app.config['UPLOAD_FOLDER'], poem.background)
                    if os.path.exists(old_background_path):
                        os.remove(old_background_path)
            # Assign the new background
            poem.background = new_background
        if 'delete_background' in request.form:
            if poem.background:
                # Check if the background image is used by other poems or arts
                other_poems_using_image = Poem.query.filter(Poem.id != poem.id, Poem.background == poem.background).count()
                arts_using_image = Art.query.filter_by(art_upload=poem.background).count()
                if other_poems_using_image == 0 and arts_using_image == 0:
                    # Remove the existing background file from the server
                    background_path = os.path.join(current_app.config['UPLOAD_FOLDER'], poem.background)
                    if os.path.exists(background_path):
                        os.remove(background_path)
                # Remove the background reference from the poem
                poem.background = None
        poem.title = form.title.data
        poem.content = form.content.data
        db.session.commit()
        flash('Your poem has been updated!', 'success')
        return redirect(url_for('admin.dashboard'))
    elif request.method == 'GET':
        form.title.data = poem.title
        form.content.data = poem.content
    return render_template('create_poem.html', title='Update Poem', form=form, legend='Update Poem', poem=poem)


# Route to delete poem
@admin.route('/poem/<int:poem_id>/delete', methods=['POST'])
@login_required
def delete_poem(poem_id):
    poem = Poem.query.get_or_404(poem_id)
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
    if poem.background:
        # Check if any other poems or arts are using the same background image
        other_poems_using_image = Poem.query.filter(Poem.id != poem.id, Poem.background == poem.background).count()
        arts_using_image = Art.query.filter_by(art_upload=poem.background).count()
        if other_poems_using_image == 0 and arts_using_image == 0:
            # Remove the existing background file from the server
            background_path = os.path.join(current_app.config['UPLOAD_FOLDER'], poem.background)
            if os.path.exists(background_path):
                os.remove(background_path)
    db.session.delete(poem)
    db.session.commit()
    flash('Your poem has been deleted!', 'success')
    return redirect(url_for('admin.dashboard'))


# Art upload and gallery routes
@admin.route('/admin/upload_art', methods=['GET', 'POST'])
@login_required
def upload_art():
    if not current_user.is_admin:
        return redirect(url_for('main.index'))
    form = UploadArtForm()
    if form.validate_on_submit():
        title = form.title.data
        if form.art_upload.data:
            art_file = form.art_upload.data
            filename = save_image(art_file)
            new_art = Art(title=title, art_upload=filename)
            db.session.add(new_art)
            db.session.commit()
            # Notify subscribers
            subject = "New Art Added"
            body = """Hello, 

I just added new art to my collection.  Come check it out!
https://brittaniwrotethis.pythonanywhere.com/art_gallery

If you wish to unsubscribe at any time, please click the link below:
https://brittaniwrotethis.pythonanywhere.com/subscribe, enter your email and click unsubscribe.

Thank you for your support!

Best regards,
Brittani Collette x
                    """
            send_update_email(subject, body)
            flash('Your art has been uploaded and your subscribers were notified!', 'success')
            return redirect(url_for('admin.dashboard'))
    return render_template('upload_art.html', title='Upload Art', form=form)


# Route to update existing art
@admin.route('/art/<int:art_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_art(art_id):
    art = Art.query.get_or_404(art_id)
    form = UploadArtForm()
    if form.validate_on_submit():
        art.title = form.title.data
        if form.art_upload.data:
            art.art_upload = save_image(form.art_upload.data)
        db.session.commit()
        flash('Your art has been updated!', 'success')
        return redirect(url_for('admin.dashboard'))
    elif request.method == 'GET':
        form.title.data = art.title
    return render_template('upload_art.html', title='Edit Art', form=form, legend='Edit Art', art=art)


# Route to delete art
@admin.route('/art/<int:art_id>/delete', methods=['POST'])
@login_required
def delete_art(art_id):
    art = Art.query.get_or_404(art_id)
    if art.art_upload:
        # Check if any poems or other arts are using the same image
        poems_using_image = Poem.query.filter_by(background=art.art_upload).count()
        other_arts_using_image = Art.query.filter(Art.id != art.id, Art.art_upload == art.art_upload).count()
        if poems_using_image == 0 and other_arts_using_image == 0:
            # Remove the existing art file from the server
            art_path = os.path.join(current_app.config['UPLOAD_FOLDER'], art.art_upload)
            if os.path.exists(art_path):
                os.remove(art_path)
    db.session.delete(art)
    db.session.commit()
    flash('Your art has been deleted!', 'success')
    return redirect(url_for('admin.dashboard'))
