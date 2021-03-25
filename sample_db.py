from webapp import db
from webapp import Users, Projects, Skills, Applications, csField

db.create_all()


user_1 = Users(
    #user_id=1,
    first_name='daniel',
    last_name='bae',
    email_address="dan@gmail.com",
    is_moderator=True,
    skill_id=1,
    # skill_1_id=14,
    # skill_1_proficiency=4,
    # skill_2_id=11,
    # skill_2_proficiency=3,
    # skill_3_id=12,
    # skill_3_proficiency=2,
)

#db.session.add(user_1)

user_2 = Users(
    # user_id=3,
    first_name='simon',
    last_name='says',
    email_address="jeff@gmail.com",
    is_moderator=True,
    skill_id=1,
    # skill_1_proficiency=3,
    # skill_2_id=6,
    # skill_2_proficiency=4,
    # skill_3_id=1,
    # skill_3_proficiency=2,
)

#db.session.add(user_2)
#db.session.commit()


skill_1 = Skills(
    # skill_id=1,
    skill_name="Python",
    skill_desc="An general purpose Object Oriented language",
)

skill_2 = Skills(
    skill_name="C++",
    skill_desc="Low Level Programming Language",
)

#db.session.add(skill_1)
db.session.add(skill_2)
db.session.commit()
