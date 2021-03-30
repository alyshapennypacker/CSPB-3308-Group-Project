""" Sample Operations on Tables


Goal: test the following cases with queries
- Query exising entries in DB
- Testing relationships between Tables
- Adding objects into our DB


Note: children (Users) inherit attributes from parent(Skills) tables 
"""

from webapp import db
from webapp import Users, Projects, Skills, csField, UserProjects
from sqlalchemy import or_


# 1) convert all rows Users into: a list of objects
# #-----------------------------------------------------------------------
user_rows = Users.query.all()
print(f"{type(user_rows)} \n{user_rows} \n")

for user in user_rows:
    print(f'row: {user}')
print("-"*50)


# 2) Find all users names of people
skill_python = Skills.query.filter_by(name='Python').first()
# #-----------------------------------------------------------------------
# Option 2A) using relationship on skills tables "users" (commented out in webapp.py)
for person in skill_python.users:
    print(f"python users: {person.first_name} {person.last_name}")

# Option 2B) filtering users by skill id
python_users = Users.query.filter(or_(Users.skill_id_1 == skill_python.id,
                                      Users.skill_id_2 == skill_python.id,
                                      Users.skill_id_3 == skill_python.id))
for person in python_users:
    print(f"python users:{person.first_name} {person.last_name}")


# 3) Find the name and description of skills, for some_user
# #-----------------------------------------------------------------------
# Now we have full access to all of attributes of Skill
some_user = Users.query.filter_by(first_name='daniel').first()
print(some_user.skill_1)
print(some_user.skill_1.name)
print(some_user.skill_1.desc)
print(some_user.skill_1.image)
print(some_user.skill_2)
print(some_user.skill_2.name)
print(some_user.skill_3)
print(some_user.skill_3.name)
print(some_user.allskills)

# secondary join to reduce the need for 3 columns for each skill
# actors = db.relationship("Actor", secondary=actors, backref="movies", lazy="select")


# 4) Testing junction table
# #-----------------------------------------------------------------------
# Pull all users from projects tables
# - Using .relationship() named "project_members" found on Projects table
project_rows = Projects.query.all()
for project in project_rows:
    print(project.__repr__())
    for idx, member in enumerate(project.project_members):
        print(f'\t i={idx}: {member.__repr__()})')

# Bi-Direction: Pull all projects a given user is on
# - Using backref named "user_projects", ~invisble column on Users table
for user in user_rows:
    print(f"{user.__repr__()}")
    for idx, project in enumerate(user.user_projects):
        print(f'\t i={idx}: {project.__repr__()})')


# #5) Adding new rows using pythonic lists (append, extend)
# #-----------------------------------------------------------------------
# new_project = Projects(name="Machine learning noobs",
#                        desc="looking for other noobs to develop machine learning skills with")
# db.session.add(new_project)
# db.session.commit()

# skill_vim = Skills(name="Vim", desc="A text editor")
# skill_vs = Skills(name="vscode", desc="A text editor")
# skill_note = Skills(name="notepad", desc="A text editor")

# new_user = Users(first_name='vim', last_name='god', email="vimgod@vim.com",
#                  skill_id_1=skill_vim.id,
#                  skill_proficiency_1=4,
#                  skill_id_2=1,
#                  skill_proficiency_2=3,
#                  skill_id_3=2,
#                  skill_proficiency_3=2
#                  )
# new_user_2 = Users(first_name='vscode', last_name='champ', email="not_vimgod@vs.com",
#                    skill_id_1=skill_vs.id,
#                    skill_proficiency_1=4,
#                    skill_id_2=1,
#                    skill_proficiency_2=3,
#                    skill_id_3=2,
#                    skill_proficiency_3=2
#                    )
# new_user_3 = Users(first_name='notepad', last_name='OG', email="whatsvim@og.com",
#                    skill_id_1=skill_note.id,
#                    skill_proficiency_1=4,
#                    skill_id_2=1,
#                    skill_proficiency_2=3,
#                    skill_id_3=2,
#                    skill_proficiency_3=2
#                    )
# new_project.project_members.append(new_user)
# new_project.project_members.extend((new_user_2, new_user_3))
# db.session.commit()
