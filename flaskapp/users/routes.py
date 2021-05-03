from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp import db, bcrypter
from flaskapp.models import Users, Projects
from flaskapp.users.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskapp.users.utils import save_picture_helper

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    """ Validate user submission, then re-direct to home page 

    Validate:
        - Form fields contstraints
        - Database: Confirm user is not duplicate"""

    form = RegistrationForm()
    if form.validate_on_submit() and request.method == 'POST':
        hashed_password = bcrypter.generate_password_hash(form.password.data).decode('utf-8')
        user = Users(password=hashed_password, email=form.email.data,
                     first_name=form.firstname.data, last_name=form.lastname.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.firstname.data} {form.lastname.data}!', category='success')
        return redirect(url_for('main.home'))

    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    """ Valididate User submission, then login current_user, otherwise provide feedback
    - Re-directs users to pages which required login access (next_page)

    Validate:
        - Form field contstraints
        - Database: Confirm user has an account """

    form = LoginForm()
    if current_user.is_authenticated:  # if already logged in
        return redirect(url_for('main.home'))

    # Validate login fields in database
    if form.validate_on_submit() and request.method == 'POST':
        form_email, form_password = form.email.data, form.password.data
        db_user = Users.query.filter_by(email=form_email).first()
        if db_user and bcrypter.check_password_hash(pw_hash=db_user.password, password=form_password):
            login_user(db_user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Successfully logged in. Welcome {db_user.first_name} {db_user.last_name}!', category='success')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Unable to login. Email and password combination does not match/exist', category='danger')

    return render_template('login.html', title='Login', form=form)


@users.route("/logout")
def logout():
    flash(f"Successfully Logged out {current_user.first_name}!", category='success')
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    ''' User account route '''

    form = UpdateAccountForm()
    if form.validate_on_submit() and request.method == 'POST':
        if form.picture.data:  # Save and Set profile picture
            picture_file = save_picture_helper(form.picture.data)
            current_user.profile_image = picture_file

        current_user.first_name = form.firstname.data
        current_user.last_name = form.lastname.data
        current_user.email = form.email.data
        db.session.commit()
        flash("You've successfully updated your account!", category="success")
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.firstname.data = current_user.first_name
        form.lastname.data = current_user.last_name

    image_file = url_for('static', filename=f'/profile_pics/{current_user.profile_image}')

    return render_template('account.html', title='Account', image_file=image_file, form=form)
