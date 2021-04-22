from sqlalchemy.sql.expression import desc
from flaskapp.models import Users, Projects, Languages, Careers, UserProjects, UserLanguages, UserCareers, ProjectLanguages, ProjectCareers
from sqlalchemy import or_

def bootstrap_helper(db):
    ''' Actually populates database with sample data '''

    # ---------- Add `Role`s ----------
    CareersNames = ['Developer, back-end', 'Developer, full-stack', 'Developer, front-end', 'Developer, desktop or enterprise applications', 'Developer, mobile',
                 'DevOps specialist', 'Database administrator', 'Designer', 'System administrator', 'Developer, embedded applications or devices', 'Data or business analyst',
                 'Data scientist or machine learning specialist', 'Developer, QA or test', 'Engineer, data', 'Academic researcher', 'Educator', 'Developer, game or graphics',
                 'Engineering manager', 'Product manager', 'Scientist', 'Engineer, site reliability', 'Senior executive/VP', 'Marketing or sales professional']
    survey_Careers = [Careers(name=str(name)) for name in CareersNames]
    db.session.add_all(survey_Careers)
    db.session.commit()

    career_backend = Careers.query.filter_by(name="Developer, back-end").first()
    career_fullstack = Careers.query.filter_by(name="Developer, full-stack").first()
    career_design = Careers.query.filter_by(name="Designer").first()

    # ---------- Add Languages ----------
    languageNames = ['JavaScript', 'HTML/CSS', 'SQL', 'Python', 'Java', 'Bash/Shell/PowerShell', 'C#', 'PHP', 'C++', 'TypeScript', 'C', 'Ruby', 'Go',
                    'Assembly', 'Swift', 'Kotlin', 'R', 'VBA', 'Objective-C', 'Scala', 'Rust', 'Dart', 'Elixir', 'Clojure', 'WebAssembly']
    languages = [Languages(name=str(name)) for name in languageNames]
    db.session.add_all(languages)
    db.session.commit()

    language_python = Languages.query.filter_by(name="Python").first()
    language_cpp = Languages.query.filter_by(name="C++").first()
    language_js = Languages.query.filter_by(name="JavaScript").first()
    language_kotlin = Languages.query.filter_by(name="Kotlin").first()
    
    # ---------- Add Users ----------
    user_1 = Users(first_name='daniel', last_name='bae', email="dan@gmail.com", password="hashed_password")
    user_2 = Users(first_name='simon', last_name='says', email="jeff@gmail.com", password="hashed_password")
    user_3 = Users(first_name='jeff', last_name='williams', email="jw@gmail.com", password="hashed_password")
    db.session.add_all([user_1, user_2, user_3])
    db.session.commit()

    user_1_query = Users.query.filter_by(first_name="daniel").first()
    user_2_query = Users.query.filter_by(first_name="simon").first()
    user_3_query = Users.query.filter_by(first_name="jeff").first()

    # ---- Add User's Languages w/ pythonic lists functionality ----
    user_1.languages.extend((language_python,language_cpp,language_js))
    user_2.languages.extend((language_python,language_kotlin))
    user_3.languages.extend((language_python,language_cpp,language_js,language_kotlin))
    # ---- Add Users's Careers w/ pythonic lists functionality ----
    user_1.careers.extend((career_backend,career_fullstack,career_design))
    user_2.careers.extend((career_backend,career_fullstack))
    user_3.careers.extend((career_backend,career_design))
    db.session.commit()

    

    # ---------- Add Projects ----------
    project_1 = Projects(name="Lets make a React App!!!", desc="Welcome all levels of exp, just looking to get expossure to react",
                         owner_id=user_2.id)
    project_2 = Projects(name="Anyone looking to get started with mobile development?", desc="Currently interested in Koitlin dev, but open to other stacks as well!",
                         owner_id=user_2.id)
    db.session.add_all([project_1, project_2])
    db.session.commit()

    # ---- Adding Project's Members w/ pythonic lists functionality ----
    project_1.members.extend((user_1, user_2, user_3))
    project_2.members.append(user_3)
    # ---- Adding Project's Languages w/ pythonic lists functionality ----
    project_1.languages.extend((language_python,language_cpp,language_js))
    project_2.languages.extend((language_python,language_kotlin))
    # ---- Adding Project's Careers w/ pythonic lists functionality ----
    project_1.careers.extend((career_backend,career_fullstack,career_design))
    project_2.careers.extend((career_backend,career_fullstack))

    db.session.commit()


def query_helper(db):
    print("Object Relational Mappers(SQLAlchemy) represent tables as a List of Objects\n")

    user_rows = Users.query.all()
    print("1) Convert all rows in Users table, into a list of objects")
    print(f"user_rows type = {type(user_rows)}")
    for user in user_rows:
        print(f'\t row: {user}')
    print("-"*100)

    print("2) Find all python users (contain skill Python)\n")
    language_python = Languages.query.filter_by(name='Python').first()
    python_users = Users.query.filter(or_(Users.skill_id_1 == language_python.id,
                                        Users.skill_id_2 == language_python.id,
                                        Users.skill_id_3 == language_python.id))
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
    # tableClasses = [Roles, Industries, ProjectInterests]
    tableClasses = [Careers]


    def printTest(tableClasses):
        print("4) Checking many to many relationships of the tables [CareersName]\n")
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