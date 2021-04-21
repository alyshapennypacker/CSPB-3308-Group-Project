from flask import render_template, url_for, flash, redirect
from flaskapp import app, db, bcrypter
from flaskapp.models import Users, Projects, Skills, Roles, Industries, ProjectInterests, UserProjects
from flaskapp.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user


@app.route('/')
def index():
    return "hello world"


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


# source: https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/Flask_Blog/05-Package-Structure/flaskblog/routes.py
@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Validate Registration Form fields, then re-direct to home page
    - GET register.html
    - POST new entry in Users table
    """
    form = RegistrationForm()
    if form.validate_on_submit():

        hashed_password = bcrypter.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(password=hashed_password,
                     first_name='hashed user', last_name='hashed user', email="hashed@gmail.com",
                     skill_id_1=1, skill_proficiency_1=4, skill_id_2=2, skill_proficiency_2=3, skill_id_3=3, skill_proficiency_3=2,
                     role_id=1,
                     industry_id=4,
                     )
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data}!', category='success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ When current_user submits Login Form
    If valid (email,password), then login current_user
    """
    # current_user
    if current_user.is_authenticated():
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        formEmail = form.email.data
        user = Users.query.filter_by(email=formEmail).first()
        # Login user if email exists and passwords matches up
        if user and bcrypter.check_password_hash(form.password, user.password):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', category='danger')
    return render_template('login.html', title='Login', form=form)
