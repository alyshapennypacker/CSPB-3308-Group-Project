import secrets
import os
from PIL import Image

from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp import app, db, bcrypter
from flaskapp.models import Users, Projects, Languages, Careers, UserProjects, UserLanguages, UserCareers,  ProjectLanguages, ProjectCareers
from flaskapp.forms import RegistrationForm, LoginForm, UpdateAccountForm


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

# source: https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/Flask_Blog/05-Package-Structure/flaskblog/routes.py
@app.route('/register', methods=['GET', 'POST'])
def register():
    """ Validate user submission, then re-direct to home page 
    
    Validate:
        - Form fields contstraints
        - Database: Confirm user is not duplicate"""

    form = RegistrationForm()
    if form.validate_on_submit() and request.method == 'POST':
        hashed_password = bcrypter.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(password=hashed_password, email=form.email.data, first_name=form.firstname.data, last_name=form.lastname.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.firstname.data} {form.lastname.data}!', category='success')
        return redirect(url_for('home'))
    
    elif request.method == 'GET':
        form.email.data = "first.last@colorado.edu"
    return render_template('register.html', title='Register', form=form)

        

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Valididate User submission, then login current_user, otherwise provide feedback
    - Re-directs users to pages which required login access (next_page)

    Validate:
        - Form field contstraints
        - Database: Confirm user has an account """

    form = LoginForm()    
    if current_user.is_authenticated:  # if already logged in
        return redirect(url_for('home'))
    
    # Validate login fields in database
    if form.validate_on_submit() and request.method == 'POST':
        form_email, form_password = form.email.data, form.password.data
        db_user = Users.query.filter_by(email=form_email).first()
        if db_user and bcrypter.check_password_hash(pw_hash=db_user.password, password=form_password):
            login_user(db_user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Successfully logged in. Welcome {db_user.first_name} {db_user.last_name}!', category='success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Unable to login. Email and password combination does not match/exist', category='danger')

    elif request.method == 'GET':
        form.email.data = "first.last@colorado.edu"   
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    flash(f"Successfully Logged out {current_user.first_name}!", category='success')
    logout_user()
    return redirect(url_for('home'))
    


def save_picture_helper(form_picture):
    ''' helper function which
    1) Takes pictures field (.jpg, .png) submitted on form
    2) Set save location for picures
    3) Resize and save image '''
    
    # creating unique name when saving pictures
    rand_hex = secrets.token_hex(nbytes=8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_filename = rand_hex + file_ext
    # Setting file path for save location
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_filename)

    # image resizing and saving
    output_size = (125,125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_filename

@app.route("/account", methods=['GET','POST']) 
@login_required
def account():
    ''' User account route '''
    form = UpdateAccountForm()
    
    # Updating profile informaiton 
    if form.validate_on_submit():
        # Save and Set profile picture
        if form.picture.data:
            picture_file = save_picture_helper(form.picture.data)
            current_user.profile_image = picture_file

        current_user.first_name = form.firstname.data
        current_user.last_name = form.lastname.data
        current_user.email = form.email.data
        db.session.commit()
        flash("You've successfully updated your account!", category="success")
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.firstname.data = current_user.first_name
        form.lastname.data = current_user.last_name

    image_file = url_for('static', filename=f'/profile_pics/{current_user.profile_image}')

    return render_template('account.html', title='Account',image_file=image_file, form=form)


@app.route('/register/languages', methods=['GET', 'POST'])
def register_languages():
    return f"register languages here"

@app.route('/register/careers', methods=['GET', 'POST'])
def register_careers():
    return f"register careers here"


@app.route("/projects")
def projects():
    return render_template('projects.html', title='Account')


@app.route("/projects/create", methods=['GET', 'POST'])
def projects_create():
    return f"Create careers here"

@app.route("/projects/<int:post_id>", methods=['GET', 'POST'])
def projects_view(post_id):
    return 'Post %d' % post_id
