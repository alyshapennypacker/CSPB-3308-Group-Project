from flask import render_template, url_for, flash, redirect
from flaskapp import app
from flaskapp.forms import RegistrationForm, LoginForm
from flaskapp.models import Users, Projects


@ app.route('/')
@ app.route('/home')
def home():
    return render_template('home.html')


@ app.route('/about')
def about():
    return render_template('about.html')


# source: https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/Flask_Blog/05-Package-Structure/flaskblog/routes.py
@app.route("/register", methods=['GET', 'POST'])
def register():
    """
    Validate Registration Form fields, then re-direct to home page
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', category='success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Validate Login Form fields:
    - then, re-direct to home page
    - else, output unsuccesful 
    """
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', category='success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', category='danger')
    return render_template('login.html', title='Login', form=form)
