from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp import app, db, bcrypter
from flaskapp.models import Users, Projects, Languages, Careers, UserProjects, UserLanguages, UserCareers,  ProjectLanguages, ProjectCareers
from flaskapp.forms import RegistrationForm, LoginForm


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
    """ If valid upon submission then re-direct to home page 
    
    Validate:
        - Form fields contstraints
        - Database: Confirm user is not duplicate"""

    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('register.html', title='Register', form=form)

    elif request.method == 'POST':
        if form.validate_on_submit():
            hashed_password = bcrypter.generate_password_hash(form.password.data).decode('utf-8')
            user = Users(password=hashed_password, email=form.email.data, first_name=form.firstname.data, last_name=form.lastname.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Account created for {form.firstname.data} {form.lastname.data}!', category='success')
            return redirect(url_for('home'))

        

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ If valid upon submission, then login current_user, otherwise provide feedback
    
    Validate:
        - Form field contstraints
        - Database: Confirm user has an account """

    form = LoginForm()    
    if request.method == 'GET':
        return render_template('login.html', title='Login', form=form)

    elif request.method == 'POST':
        if current_user.is_authenticated:  # if already logged in
            return redirect(url_for('home'))
        if form.validate_on_submit():
            form_email, form_password = form.email.data, form.password.data
            db_user = Users.query.filter_by(email=form_email).first()
            db_hashed_password = db_user.password
            if db_user and bcrypter.check_password_hash(db_hashed_password,form_password):
                login_user(db_user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Unable to login. Email and password combination does not match/exist', category='danger')
        

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
    
@app.route("/account")
@login_required # login_req Decorator requires login to access route
def account():
    return render_template('account.html', title='Account')


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
