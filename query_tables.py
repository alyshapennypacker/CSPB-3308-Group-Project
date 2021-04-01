""" Sample Operations on Tables


Goal: test the following cases with queries
- Query exising entries in DB
- Testing relationships between Tables
- Adding objects into our DB


Note: children (Users) inherit attributes from parent(Skills) tables 
"""
from webapp import db, Users, Projects, Skills, Roles, Industries, ProjectInterests, UserProjects
from sqlalchemy import or_
print("Object Relational Mappers(SQLAlchemy) represent tables as a List of Objects\n")

user_rows = Users.query.all()
print("1) Convert all rows in Users table, into a list of objects")
print(f"user_rows type = {type(user_rows)}")
for user in user_rows:
    print(f'\t row: {user}')


print("2) Find all python users (contain skill Python)\n")
skill_python = Skills.query.filter_by(name='Python').first()
python_users = Users.query.filter(or_(Users.skill_id_1 == skill_python.id,
                                      Users.skill_id_2 == skill_python.id,
                                      Users.skill_id_3 == skill_python.id))
for person in python_users:
    print(f"python users:{person.first_name} {person.last_name}")
print("-"*100)

print("3) Testing Many to Many relationship\n")
print("Pull all users a given project")
project_rows = Projects.query.all()
for project in project_rows:
    print(project)
    for idx, member in enumerate(project.members):
        print(f'\t i={idx}: {member})')

print("\nBi-Direction: Pull all projects for a given user")
for user in user_rows:
    print(user)
    for idx, project in enumerate(user.get_projects):
        print(f'\t i={idx}: {project})')
print("-"*100)


# 4) Testing 1 to many Relationships of <table>
# <table> to many user
# <table> to many projects
tableClasses = [Roles, Industries, ProjectInterests]


def printTest(tableClasses):
    print("Checking many to many relationships of the tables [Roles, Industries, ProjectInterests]\n")
    for table in tableClasses:
        # Iterate through each row in specified <table>
        table_rows = table.query.all()
        for object_instance in table_rows:
            # object.(user/project) contains all the f-keys in Users and Projects
            print(object_instance)
            for idx, user in enumerate(object_instance.users):  # Print each User tagged
                print(f'\t i={idx}: {user})')
            for idx, project in enumerate(object_instance.projects):  # Print each Project tagged
                print(f'\t i={idx}: {project})')


printTest(tableClasses)
