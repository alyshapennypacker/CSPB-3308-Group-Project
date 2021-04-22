from flask import render_template, url_for, flash, redirect, request
from flaskapp import app, db, bcrypter
from flaskapp.models import Users, Projects, Languages, Careers, UserProjects, UserLanguages, UserCareers,  ProjectLanguages, ProjectCareers
from flaskapp.forms import RegistrationForm, LoginForm

# flask_login - functions tp manage user sessions
from flask_login import login_user, current_user, logout_user, login_required



@app.route('/loginn', methods=['GET', 'POST'])
def loginn():
    if request.method == 'POST':
        user = request.form['name']
        return redirect(url_for("user", usr_x=user))
    elif request.method == 'GET':
        return render_template('loginn.html')
    
@app.route("/<usr_x>")
def user(usr_x):
    return f"<h1>{usr_x}</h1>"
    




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
    """
    Validate Registration Form fields, then re-direct to home page
    - GET register.html
    - POST new entry in Users table
    """
    form = RegistrationForm()
    if form.validate_on_submit():

        hashed_password = bcrypter.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(password=hashed_password, email=form.email.data,
                     first_name='hashed user', last_name='hashed user',)
                    #  skill_id_1=1, skill_proficiency_1=4, skill_id_2=2, skill_proficiency_2=3, skill_id_3=3, skill_proficiency_3=2,
                    #  role_id=1, industry_id=4,
                    #  )
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
    # Re-direct back to home page if already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = LoginForm()
    if form.validate_on_submit():
        form_email, form_password = form.email.data, form.password.data
        form_user = Users.query.filter_by(email=form_email).first()
        # If email exists and passwords matches up, then Login user and 
        if form_user and bcrypter.check_password_hash(form_user.password,form_password):
            login_user(form_user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Unable to login. Email and password combination does not match/exist', category='danger')
    return render_template('login.html', title='Login', form=form)
    


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required # login_req Decorator requires login to access route
def account():
    return render_template('account.html', title='Account')

@app.route("/projects")
def projects():
    return render_template('projects.html', title='Account')