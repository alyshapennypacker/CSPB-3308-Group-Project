from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

from tests import bootstrap_tables

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Supress deprecation message
db = SQLAlchemy(app)


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Supress deprecation message
    db.init_app(app)

    with app.app_context():
        # needed to make CLI commands work
        from . import commands
        return app

@app.cli.command("drop")
def reset_db():
    ''' Drops all tables in database '''
    db.drop_all()
    print("Dropped DB tables")


@app.cli.command("bootstrap")
def bootstrap_data():
    ''' Populates database with some sample data '''
    db.drop_all()
    db.create_all()
    # bootstrap_tables.populate_tables(db)
    bootstrap_helper(db)
    print("Initialized clean DB tables and Bootstrapped with data")


@ app.route('/')
@ app.route('/home')
def home():
    return "hello"
    #return render_template('home.html')

# source: https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/Flask_Blog/05-Package-Structure/flaskblog/routes.py
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


# source: https://github.com/CoreyMSchafer/code_snippets/blob/master/Python/Flask_Blog/05-Package-Structure/flaskblog/routes.py
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)




# Association table: automatically updates based on Users and Projects tables (https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html#many-to-many)
UserProjects = db.Table("userproject",
                        db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
                        db.Column("project_id", db.Integer, db.ForeignKey("project.id"), primary_key=True))


class Users(db.Model):
    ''' Users Table:
    User profile information and Fact table (collection of many foreign keys)
    '''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_image = db.Column(db.String(20), nullable=False, default="profile.jpg")
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_moderator = db.Column(db.Boolean, default=False, nullable=False)
    skill_proficiency_1 = db.Column(db.Integer, nullable=False)
    skill_proficiency_2 = db.Column(db.Integer, nullable=False)
    skill_proficiency_3 = db.Column(db.Integer, nullable=False)

    # Skills - Multiple foriegn keys to one table
    skill_id_1 = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    skill_id_2 = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    skill_id_3 = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    skill_1 = db.relationship("Skills", foreign_keys=skill_id_1)
    skill_2 = db.relationship("Skills", foreign_keys=skill_id_2)
    skill_3 = db.relationship("Skills", foreign_keys=skill_id_3)

    # CS Career Goal (top choice)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False, default=1)
    career = db.relationship("Roles", foreign_keys=role_id, backref="users")
    # Target Industries for user - top choice(s) # Industries,industry
    industry_id = db.Column(db.Integer, db.ForeignKey('industry.id'), nullable=False, default=1)
    industry = db.relationship("Industries", foreign_keys=industry_id, backref="users")
    # ProjectInterests (top choice)
    projectinterest_id = db.Column(db.Integer, db.ForeignKey('projectinterest.id'), nullable=False, default=1)
    interest = db.relationship("ProjectInterests", foreign_keys=projectinterest_id, backref="users")

    def __repr__(self):
        return f"User('{self.first_name}', '{self.last_name}', '{self.email}')"


class Projects(db.Model):
    ''' Projects Table:
    Group projects a user can post
    '''
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(250), unique=True, nullable=False)
    desc = db.Column(db.String(500), unique=False, nullable=False)
    creation_timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    start_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    target_end_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, default=1)
    owner = db.relationship("Users", foreign_keys=owner_id, backref="owned_projects", uselist=False)
    members = db.relationship('Users', secondary=UserProjects, lazy='subquery', backref="get_projects")

    # Related CS roles to project (top choice)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False, default=1)
    roles = db.relationship("Roles", foreign_keys=role_id, backref="projects")
    # Industry context related to project
    industry_id = db.Column(db.Integer, db.ForeignKey('industry.id'), nullable=False, default=1)
    industry = db.relationship("Industries", foreign_keys=industry_id, backref="projects")
    # ProjectInterests (top choice)
    projectinterest_id = db.Column(db.Integer, db.ForeignKey('projectinterest.id'), nullable=False, default=1)
    interest = db.relationship("ProjectInterests", foreign_keys=projectinterest_id, backref="projects")

    def __repr__(self):
        return f"Project[ID:'{self.id}', Name:'{self.name}'] "


class Skills(db.Model):
    ''' Skills Table:
    Common technical skills per StackOverflow 2019 survey
    '''
    __tablename__ = 'skill'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    desc = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(20), nullable=False, default="skill.jpg")

    def __repr__(self):
        return f"Skill('{self.name}', '{self.desc}')"


class Roles(db.Model):
    ''' Roles Table:
    Common SWE related Roles per StackOverflow 2019 survey
    '''
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    desc = db.Column(db.String(250), nullable=False, default="wikisnippet")
    image = db.Column(db.String(20), nullable=False, default="Roles.jpg")

    def __repr__(self):
        return f"Roles('{self.name}', '{self.desc}')"


class Industries(db.Model):
    ''' Industries Table:
    SW related Industries per StackOverflow 2019 survey
    '''
    __tablename__ = 'industry'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    desc = db.Column(db.String(250), nullable=False, default="wikisnippet")
    image = db.Column(db.String(20), nullable=False, default="Industries.jpg")

    def __repr__(self):
        return f"Industries('{self.name}', '{self.desc}')"


class ProjectInterests(db.Model):
    ''' Interests Table:
    A users general interests in Technologies, related to projects 
    (ex. Computer vision, Robotics, Cloud, etc.)
    '''
    __tablename__ = 'projectinterest'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    desc = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(20), nullable=False, default="ProjectInterests.jpg")

    def __repr__(self):
        return f"ProjectInterests('{self.name}', '{self.desc}')"


# ----------------------------------------------------------------------------------------------------------------------------
def bootstrap_helper(db):
    ''' Actually populates database with sample data '''
    # ---------- Add Skills ----------
    skill_python = Skills(name="Python", desc="An general purpose Object Oriented language")
    skill_cpp = Skills(name="C++", desc="Low Level Programming Language")
    skill_3 = Skills(name="Javascript", desc="Web Development Language")
    skill_4 = Skills(name="Koitlin", desc="Mobile development")
    db.session.add_all([skill_python, skill_cpp, skill_3, skill_4])
    db.session.commit()

    # ---------- Add Users ----------
    user_1 = Users(first_name='daniel', last_name='bae', email="dan@gmail.com",
                   skill_id_1=skill_python.id, skill_proficiency_1=4, skill_id_2=skill_cpp.id, skill_proficiency_2=3, skill_id_3=skill_3.id, skill_proficiency_3=2,
                   role_id=1,
                   industry_id=4,
                   )
    user_2 = Users(first_name='simon', last_name='says', email="jeff@gmail.com",
                   skill_id_1=skill_cpp.id, skill_proficiency_1=3, skill_id_2=skill_python.id, skill_proficiency_2=4, skill_id_3=skill_4.id, skill_proficiency_3=2,
                   role_id=5,
                   industry_id=1,
                   )
    user_3 = Users(first_name='jeff', last_name='williams', email="jw@gmail.com",
                   skill_id_1=skill_4.id, skill_proficiency_1=3, skill_id_2=skill_3.id, skill_proficiency_2=4, skill_id_3=skill_cpp.id, skill_proficiency_3=2,
                   role_id=2,
                   industry_id=2,
                   )
    db.session.add_all([user_1, user_2, user_3])
    db.session.commit()

    # ---------- Add Projects ----------
    project_1 = Projects(name="Lets make a React App!!!", desc="Welcome all levels of exp, just looking to get expossure to react",
                         owner_id=user_2.id
                         )
    project_2 = Projects(name="Anyone looking to get started with mobile development?", desc="Currently interested in Koitlin dev, but open to other stacks as well!",
                         owner_id=user_2.id
                         )
    db.session.add_all([project_1, project_2])
    db.session.commit()

    # ---------- Adding (rows) Project Members w/ pythonic lists functionality ----------
    project_1.members.extend((user_1, user_2, user_3))
    project_2.members.append(user_3)
    db.session.commit()

    # ---------- Add Industries ----------
    industryNames = ['Software development - other', 'Information technology', 'Financial and banking', 'Software as a service (saas) development', 'Web development or design', 'Consulting',
                     'Data and analytics', 'Health care or social services', 'Media, advertising, publishing, or entertainment', 'Retail or ecommerce',
                     'Internet', 'Education and training', 'Manufacturing', 'Cloud-based solutions or services', 'Government or public administration', 'Research - academic or scientific',
                     'Telecommunications', 'Transportation', 'Energy or utilities', 'Security', 'Marketing', 'Travel', 'Nonprofit', 'Real estate']
    survey_industries = [Industries(name=str(name)) for name in industryNames]
    db.session.add_all(survey_industries)
    db.session.commit()

    # ---------- Add Roles ----------
    roleNames = ['Developer, back-end', 'Developer, full-stack', 'Developer, front-end', 'Developer, desktop or enterprise applications', 'Developer, mobile',
                 'DevOps specialist', 'Database administrator', 'Designer', 'System administrator', 'Developer, embedded applications or devices', 'Data or business analyst',
                 'Data scientist or machine learning specialist', 'Developer, QA or test', 'Engineer, data', 'Academic researcher', 'Educator', 'Developer, game or graphics',
                 'Engineering manager', 'Product manager', 'Scientist', 'Engineer, site reliability', 'Senior executive/VP', 'Marketing or sales professional']

    survey_roles = [Roles(name=str(name)) for name in roleNames]
    db.session.add_all(survey_roles)
    db.session.commit()

    # ---------- Add ProjectInterests ----------
    interest_1 = ProjectInterests(name="Medical", desc="Genteics, Medical imaging, etc.")
    interest_2 = ProjectInterests(name="Space", desc="Simulations, Robotics, Computer vision")
    db.session.add_all([interest_1, interest_2])
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
