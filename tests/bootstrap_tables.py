from webapp import db
from webapp import Users, Projects, Skills, ProjectInterests, csField


class bootstrap_helper:
    def populate_tables(self):
        ''' Actually populates database with data '''
        # Test Skills
        # --------------------------------------------------------------
        skill_python = Skills(name="Python",
                              desc="An general purpose Object Oriented language")
        skill_cpp = Skills(name="C++",
                           desc="Low Level Programming Language")
        skill_3 = Skills(name="Javascript",
                         desc="Web Development Language")
        skill_4 = Skills(name="Koitlin",
                         desc="Mobile development")

        db.session.add(skill_python)
        db.session.add(skill_cpp)
        db.session.add(skill_3)
        db.session.add(skill_4)
        db.session.commit()

        # Test Users
        # --------------------------------------------------------------

        user_1 = Users(first_name='daniel',
                       last_name='bae',
                       email="dan@gmail.com",
                       skill_id_1=skill_python.id,
                       skill_proficiency_1=4,
                       skill_id_2=skill_cpp.id,
                       skill_proficiency_2=3,
                       skill_id_3=skill_3.id,
                       skill_proficiency_3=2
                       )
        user_2 = Users(first_name='simon',
                       last_name='says',
                       email="jeff@gmail.com",
                       skill_id_1=skill_cpp.id,
                       skill_proficiency_1=3,
                       skill_id_2=skill_python.id,
                       skill_proficiency_2=4,
                       skill_id_3=skill_4.id,
                       skill_proficiency_3=2
                       )
        user_3 = Users(first_name='jeff',
                       last_name='williams',
                       email="jw@gmail.com",
                       skill_id_1=skill_4.id,
                       skill_proficiency_1=3,
                       skill_id_2=skill_3.id,
                       skill_proficiency_2=4,
                       skill_id_3=skill_cpp.id,
                       skill_proficiency_3=2
                       )
        db.session.add(user_1)
        db.session.add(user_2)
        db.session.add(user_3)
        db.session.commit()

        # Test Applications
        # --------------------------------------------------------------
        interest_1 = ProjectInterests(name="Medical",
                                      desc="Genteics, Medical imaging, etc.")
        interest_2 = ProjectInterests(name="Space",
                                      desc="Simulations, Robotics, Computer vision")
        db.session.add(interest_1)
        db.session.add(interest_2)
        db.session.commit()
