from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
# from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


# Create SQLAlchemy instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


@app.route('/')
@app.route('/home')
def home():
    return "hello"


class Users(db.Model):
    ''' User Table '''
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email_address = db.Column(db.String(120), unique=True, nullable=False)
    profile_image = db.Column(db.String(20), nullable=False, default="profile.jpg")
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_moderator = db.Column(db.Boolean, default=False, nullable=False)

    #skill_1_id = db.Column(db.Integer, default=False, nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey('Skills.skill_id'), nullable=False)
    # skill_1 = db.relationship('Skills', backref='author', lazy=True)


    # skill_1_proficiency = db.Column(db.Iteger, nullable=False)
    # skill_2_id = db.Column(db.Integer, default=False, nullable=False)
    # skill_2_proficiency = db.Column(db.Integer, nullable=False)
    # skill_3_id = db.Column(db.Integer, default=False, nullable=False)
    # skill_3_proficiency = db.Column(db.Integer, nullable=False)

    # define User table's relationship, to Post table
    # - backref: auto merge user fields to posts
    # - lazy: allows us to get ALL posts for a given user
    #projects = db.relationship('Projects', backref='author', lazy=True)
 

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    # Todo: test skills first
    # career_goals = db.Column(db.String(120), unique=False, nullable=True)
    # user_cs_field_interests = string deliminiated
    # user_application_interests = string deliminated

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}')"


class Projects(db.Model):
    ''' Projects Table: containg group projects a user can post '''
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(250), unique=True, nullable=False)
    project_desc = db.Column(db.String(500), unique=False, nullable=False)
    project_creation_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    project_start_date = db.Column(db.DateTime, nullable=True)
    project_target_end_date = db.Column(db.DateTime, nullable=True)

    # Todo: test users table first
    # project_skills = string
    # project_owner_id = int

    # project_applications = string                    # Todo: test skills first
    # project_cs_field = string

    # Todo: junction table
    member_ids = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, primary_key=True)
    # members_timestamp_join = datetime corresponding to each member’s joining

    # Todo: next sprint
    # like_count = int
    # comments = tbd
    # threads = tbd


class Skills(db.Model):
    ''' Skills Table: common technical skills per StackOverflow 2019 survey '''
    skill_id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(50), unique=True, nullable=False)
    skill_desc = db.Column(db.String(250), nullable=False)
    skill_image = db.Column(db.String(20), nullable=False, default="skill.jpg")


class Applications(db.Model):
    ''' 
    Applications Table: Applications of a group project 
    - can be end-users (ex. hospital patients) 
    - can be purpose of project (ex. education) 
    '''
    application_id = db.Column(db.Integer, primary_key=True)
    application_name = db.Column(db.String(50), unique=True, nullable=False)
    application_desc = db.Column(db.String(250), nullable=False)
    application_image = db.Column(db.String(20), nullable=False, default="application.jpg")


class csField(db.Model):
    ''' 
    csField Table: 
    Common SWE related roled per StackOverflow 2019 survey 
    - examples of csfield_name {backend, frontend, mobile ,devops, etc.}
    '''
    csfield_id = db.Column(db.Integer, primary_key=True)
    csfield_name = db.Column(db.String(50), unique=True, nullable=False)
    csfield_desc = db.Column(db.String(250), nullable=False)
    csfield_image = db.Column(db.String(20), nullable=False, default="csField.jpg")


if __name__ == '__main__':
    app.run(debug=True)
