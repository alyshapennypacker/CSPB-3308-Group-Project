from app import db
from app import Users, Projects, Skills, Roles, Industries, ProjectInterests, UserProjects


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
