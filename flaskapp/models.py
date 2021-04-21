from datetime import datetime
from flaskapp import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    ''' Login manager extension '''
    return Users.query.get(int(user_id))


# Association table: automatically updates based on Users and Projects tables(https: // docs.sqlalchemy.org/en/14/orm/basic_relationships.html  # many-to-many)
UserProjects = db.Table("userproject",
                        db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
                        db.Column("project_id", db.Integer, db.ForeignKey("project.id"), primary_key=True))


# class Users(db.Model, UserMixin):
class Users(db.Model):
    ''' Users Table:
    User profile information and Fact table (collection of many foreign keys)
    UserMixin -> Adds in standard attributes/methods (ex. isAuthenticated, isActive, etc.)
    '''
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
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
