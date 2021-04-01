""" Sample Operations on Tables


Goal: test the following cases with queries
- Query exising entries in DB
- Testing relationships between Tables
- Adding objects into our DB


Note: children (Users) inherit attributes from parent(Skills) tables 
"""
from webapp import db
from webapp import Users, Projects, Skills, Roles, Industries, ProjectInterests, UserProjects
from sqlalchemy import or_


# 1) convert all rows Users into: a list of objects
# #-----------------------------------------------------------------------
print("\nObject Relational Mappers(SQLAlchemy) represent tables as a List of Objects\n")
user_rows = Users.query.all()
print(f"user_rows type = {type(user_rows)}")

for user in user_rows:
    print(f'row: {user}')
print("-"*100)


# 2) Find all users names of people
# #-----------------------------------------------------------------------
skill_python = Skills.query.filter_by(name='Python').first()
print("Query all users with skill_python as a skill\n")

# Option 2A) using relationship on skills tables "users" (deleted from webapp.py)
# for person in skill_python.users:
#     print(f"python users: {person.first_name} {person.last_name}")

# Option 2B) filtering users by skill id
python_users = Users.query.filter(or_(Users.skill_id_1 == skill_python.id,
                                      Users.skill_id_2 == skill_python.id,
                                      Users.skill_id_3 == skill_python.id))
for person in python_users:
    print(f"python users:{person.first_name} {person.last_name}")
print("-"*100)

# 3) Accessing properties
# #-----------------------------------------------------------------------
print("for some_user, Find the name and description of skills")
print("Now we have full access to all of attributes of Skill\n")
some_user = Users.query.filter_by(first_name='daniel').first()
print(some_user.skill_1)
print(some_user.skill_1.name)
print(some_user.skill_1.desc)
print(some_user.skill_1.image)
print(some_user.skill_2)
print(some_user.skill_2.name)
print(some_user.skill_3)
print(some_user.skill_3.name)
print("-"*100)


# 4) Testing junction table
# #-----------------------------------------------------------------------

# Using .relationship() named "project_members" found on Projects table
print("Query - Pull all users from projects tables\n")
project_rows = Projects.query.all()
for project in project_rows:
    print(project.__repr__())
    for idx, member in enumerate(project.members):
        print(f'\t i={idx}: {member.__repr__()})')
print("-"*50)

# Using backref "projects" (~invisble column on Users table)
print("Bi-Direction: Pull all projects a given user is on\n")
for user in user_rows:
    print(f"{user.__repr__()}")
    for idx, project in enumerate(user.get_projects):
        print(f'\t i={idx}: {project.__repr__()})')
print("-"*100)


# 5) Testing Relationships (mainlyt with Projects table)
# #-----------------------------------------------------------------------
# roles_rows
print(f"\n{'-'*10} Roles - for all roles and users tagged {'-'*10}\n")
roles_rows = Roles.query.all()
print(roles_rows)
for role in roles_rows:
    print(f"{role.__repr__()}")
    for idx, user in enumerate(role.users):
        print(f'\t i={idx}: {user.__repr__()})')

print(f"\n{'-'*10} Roles - for all Roles and all projects tagged {'-'*10}\n")
for role in roles_rows:
    print(role.__repr__())
    for project in role.projects:
        print(project.__repr__())
print("#"*100)

# Industries
print(f"\n{'-'*10} Industries - for all industry and show users tagged {'-'*10}\n")
Industries_rows = Industries.query.all()
for industry in Industries_rows:
    print(f"{industry.__repr__()}")
    for idx, user in enumerate(industry.users):
        print(f'\t i={idx}: {user.__repr__()})')

print(f"\n{'-'*10} Industries - for all industry and show projects tagged {'-'*10}\n")
for industry in Industries_rows:
    print(f"{industry.__repr__()}")
    for idx, project in enumerate(industry.projects):
        print(f'\t i={idx}: {industry.__repr__()})')
print("#"*100)

# ProjectInterests
print(f"\n{'-'*10} ProjectInterests - for all interests and all users tagged {'-'*10}\n")
interests_rows = ProjectInterests.query.all()
for interest in interests_rows:
    print(f"{interest.__repr__()}")
    for idx, user in enumerate(interest.users):
        print(f'\t i={idx}: {user.__repr__()})')

print(f"\n{'-'*10} ProjectInterests - for all interests and all projects tagged {'-'*10}\n")
for interest in interests_rows:
    print(f"{interest.__repr__()}")
    for idx, user in enumerate(interest.projects):
        print(f'\t i={idx}: {user.__repr__()})')
print("#"*100)
