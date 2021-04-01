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
user_rows = Users.query.all()
print("Object Relational Mappers(SQLAlchemy) represent tables as a List of Objects\n")
print(f"user_rows type = {type(user_rows)}")
for user in user_rows:
    print(f'\t row: {user}')
print("-"*100)


# 2) Find all users names with a skill of python
skill_python = Skills.query.filter_by(name='Python').first()
print("Query all users with skill_python as a skill\n")
python_users = Users.query.filter(or_(Users.skill_id_1 == skill_python.id,
                                      Users.skill_id_2 == skill_python.id,
                                      Users.skill_id_3 == skill_python.id))
for person in python_users:
    print(f"python users:{person.first_name} {person.last_name}")
print("-"*100)

some_user = Users.query.filter_by(first_name='daniel').first()
print(some_user.skill_1, some_user.skill_1.name, some_user.skill_2.name)
print("-"*100)


# 3) Testing Many to Many relationship
# Using .relationship() named "project_members" found on Projects table
print("Query - Pull all users from projects tables\n")
project_rows = Projects.query.all()
for project in project_rows:
    print(project)
    for idx, member in enumerate(project.members):
        print(f'\t i={idx}: {member})')
print("-"*50)

# Using backref "projects" (~invisble column on Users table)
print("Bi-Direction: Pull all projects a given user is on\n")
for user in user_rows:
    print(user)
    for idx, project in enumerate(user.get_projects):
        print(f'\t i={idx}: {project})')
print("-"*100)


# 4) Testing Relationships other 1 to many relationships
def printTest(tableClasses):
    for table in tableClasses:
        rows = table.query.all()
        for row in rows:
            print(row)
            # All users tagged
            for idx, user in enumerate(row.users):
                print(f'\t i={idx}: {user})')
            # All projects tagged
            for idx, project in enumerate(row.projects):
                print(f'\t i={idx}: {project})')


tableClasses = [Roles, Industries, ProjectInterests]
printTest(tableClasses)
