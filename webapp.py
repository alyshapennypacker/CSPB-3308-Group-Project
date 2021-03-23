from flask import Flask, render_template, url_for, flash, redirect
# from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)


# Create SQLAlchemy instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email_address = db.Column(db.String(120), unique=True, nullable=False)
    profile_image = db.Column(db.String(20), nullable=False, default="profile.jpg")
    career_goals = db.Column(db.String(120), unique=False, nullable=True)
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_moderator = db.Column(db.Boolean, default=False, nullable=False)

    skill_1_id = db.Column(db.Integer, default=False, nullable=False)
    skill_1_proficiency = db.Column(db.String(120), unique=True, nullable=False)
    skill_2_id = db.Column(db.Integer, default=False, nullable=False)
    skill_2_proficiency = db.Column(db.String(120), unique=True, nullable=False)
    skill_3_id = db.Column(db.Integer, default=False, nullable=False)
    skill_3_proficiency = db.Column(db.String(120), unique=True, nullable=False)

    # Todo: test skills first
    # user_cs_field_interests = string deliminiated
    # user_application_interests = string deliminated

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}')"


class Projects(db.Model):
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(250), unique=True, nullable=False)
    project_desc = db.Column(db.String(500), unique=False, nullable=False)
    project_creation_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    project_start_date = db.Column(db.DateTime, nullable=True)
    project_target_end_date = db.Column(db.DateTime, nullable=True)

    # Todo: test users table first
    # project_skills = string
    # project_owner_id = int

    # Todo: test skills first
    #project_applications = string
    # project_cs_field = string

    # Todo: junction table
    # member_ids = string of each members id
    # members_timestamp_join = datetime corresponding to each member’s joining

    # Todo: next sprint
    #like_count = int
    #comments = tbd
    #threads = tbd


class Skills(db.Model):
    skill_id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(50), unique=True, nullable=False)
    skill_desc = db.Column(db.String(250), nullable=False)
    skill_image = db.Column(db.String(20), nullable=False, default="skill.jpg")


class Applications(db.Model):
    application_id = db.Column(db.Integer, primary_key=True)
    application_name = db.Column(db.String(50), unique=True, nullable=False)
    application_desc = db.Column(db.String(250), nullable=False)
    application_image = db.Column(db.String(20), nullable=False, default="application.jpg")


class csField(db.Model):
    csfield_id = db.Column(db.Integer, primary_key=True)
    csfield_name = db.Column(db.String(50), unique=True, nullable=False)
    csfield_desc = db.Column(db.String(250), nullable=False)
    csfield_image = db.Column(db.String(20), nullable=False, default="csField.jpg")


@app.route('/')
@app.route('/home')
def home():
    return "hello"


if __name__ == '__main__':
    app.run(debug=True)
