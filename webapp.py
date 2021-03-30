from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask import render_template, url_for, flash, redirect
# from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Supress deprecation message
db = SQLAlchemy(app)


@app.cli.command("initdb")
def reset_db():
    ''' Drops and Creates fresh database '''
    db.drop_all()
    db.create_all()
    print("Initialized clean DB tables")


@app.cli.command("bootstrap")
def bootstrap_data():
    ''' Populates database with some sample data '''
    db.drop_all()
    db.create_all()
    bootstrap_helper()
    print("Initialized clean DB tables and Bootstrapped with data")


@ app.route('/')
@ app.route('/home')
def home():
    return "hello"


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
    careergoal_id = db.Column(db.Integer, db.ForeignKey('csfield.id'), nullable=False, default=1)
    career = db.relationship("csField", foreign_keys=careergoal_id, backref="users")

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
    owner = db.relationship("Users",
                            foreign_keys=owner_id,
                            backref="projects",
                            uselist=False)

    project_members = db.relationship('Users',
                                      secondary=UserProjects,
                                      lazy='subquery',
                                      backref="user_projects")

    # CS Career Goal (top choice)
    careergoal_id = db.Column(db.Integer, db.ForeignKey('csfield.id'), nullable=False, default=1)
    career = db.relationship("csField", foreign_keys=careergoal_id, backref="projects")

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


class csField(db.Model):
    ''' csField Table:
    Common SWE related roled per StackOverflow 2019 survey
    - examples of csfield_name {backend, frontend, mobile ,devops, etc.}
    '''
    __tablename__ = 'csfield'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    desc = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(20), nullable=False, default="csField.jpg")

    def __repr__(self):
        return f"csField('{self.name}', '{self.desc}')"


class ProjectInterests(db.Model):
    ''' Interests Table:
    Types of projects a user has preference in, for example -
    - Industries (ex. Aerospace, Finance, IoT, etc.)
    - General interests in technology (ex. Machine Learning, NLP, Autonomous vehicles)
    '''
    __tablename__ = 'projectinterest'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50), unique=True, nullable=False)
    desc = db.Column(db.String(250), nullable=False)
    image = db.Column(db.String(20), nullable=False, default="ProjectInterests.jpg")

    def __repr__(self):
        return f"ProjectInterests('{self.name}', '{self.desc}')"


# ----------------------------------------------------------------------------------------------------------------------------
def bootstrap_helper():
    ''' Actually populates database with sample data '''
    # ---------- Add Skills ----------
    skill_python = Skills(name="Python", desc="An general purpose Object Oriented language")
    skill_cpp = Skills(name="C++", desc="Low Level Programming Language")
    skill_3 = Skills(name="Javascript", desc="Web Development Language")
    skill_4 = Skills(name="Koitlin", desc="Mobile development")

    db.session.add(skill_python)
    db.session.add(skill_cpp)
    db.session.add(skill_3)
    db.session.add(skill_4)
    db.session.commit()

    # ---------- Add Users ----------
    user_1 = Users(first_name='daniel', last_name='bae', email="dan@gmail.com",
                   skill_id_1=skill_python.id,
                   skill_proficiency_1=4,
                   skill_id_2=skill_cpp.id,
                   skill_proficiency_2=3,
                   skill_id_3=skill_3.id,
                   skill_proficiency_3=2
                   )
    user_2 = Users(first_name='simon', last_name='says', email="jeff@gmail.com",
                   skill_id_1=skill_cpp.id,
                   skill_proficiency_1=3,
                   skill_id_2=skill_python.id,
                   skill_proficiency_2=4,
                   skill_id_3=skill_4.id,
                   skill_proficiency_3=2
                   )
    user_3 = Users(first_name='jeff', last_name='williams', email="jw@gmail.com",
                   skill_id_1=skill_4.id,
                   skill_proficiency_1=3,
                   skill_id_2=skill_3.id,
                   skill_proficiency_2=4,
                   skill_id_3=skill_cpp.id,
                   skill_proficiency_3=2,
                   )
    db.session.add(user_1)
    db.session.add(user_2)
    db.session.add(user_3)
    db.session.commit()

    # ---------- Add Projects ----------
    project_1 = Projects(name="Lets make a React App!!!",
                         desc="Welcome all levels of exp, just looking to get expossure to react",
                         owner=user_2.id)
    project_2 = Projects(name="Anyone looking to get started with mobile development?",
                         desc="Currently interested in Koitlin dev, but open to other stacks as well!",
                         owner=user_2.id)
    db.session.add(project_1)
    db.session.add(project_2)

    # ---------- Projects - Adding members to projects ----------
    # Adding new rows using pythonic lists functionality (append, extend)
    project_1.project_members.extend((user_1, user_2, user_3))
    project_2.project_members.append(user_3)
    db.session.commit()

    # ---------- Add Fields ----------
    field_1 = csField(name="Front-End", desc="User interface")
    field_2 = csField(name="Back-End", desc="Servers")
    db.session.add(field_1)
    db.session.add(field_2)
    db.session.commit()

    # ---------- Add ProjectInterests ----------
    interest_1 = ProjectInterests(name="Medical", desc="Genteics, Medical imaging, etc.")
    interest_2 = ProjectInterests(name="Space", desc="Simulations, Robotics, Computer vision")
    db.session.add(interest_1)
    db.session.add(interest_2)
    db.session.commit()

    # ---------- Projects - Adding members to projects and skills (Additional exxamples) ----------
    new_project = Projects(name="Machine learning noobs",
                           desc="looking for other noobs to develop machine learning skills with")
    db.session.add(new_project)
    db.session.commit()

    skill_vim = Skills(name="Vim", desc="A text editor")
    skill_vs = Skills(name="vscode", desc="A text editor")
    skill_note = Skills(name="notepad", desc="A text editor")
    db.session.add_all([skill_vim, skill_vs, skill_note])
    db.session.commit()

    new_user = Users(first_name='vim', last_name='god', email="vimgod@vim.com",
                     skill_id_1=skill_vim.id,
                     skill_proficiency_1=4,
                     skill_id_2=1,
                     skill_proficiency_2=3,
                     skill_id_3=2,
                     skill_proficiency_3=2
                     )
    new_user_2 = Users(first_name='vscode', last_name='champ', email="not_vimgod@vs.com",
                       skill_id_1=skill_vs.id,
                       skill_proficiency_1=4,
                       skill_id_2=1,
                       skill_proficiency_2=3,
                       skill_id_3=2,
                       skill_proficiency_3=2
                       )
    new_user_3 = Users(first_name='notepad', last_name='OG', email="whatsvim@og.com",
                       skill_id_1=skill_note.id,
                       skill_proficiency_1=4,
                       skill_id_2=1,
                       skill_proficiency_2=3,
                       skill_id_3=2,
                       skill_proficiency_3=2
                       )
    new_project.project_members.append(new_user)
    new_project.project_members.extend((new_user_2, new_user_3))
    db.session.commit()


if __name__ == '__main__':
    app.run(debug=True)
