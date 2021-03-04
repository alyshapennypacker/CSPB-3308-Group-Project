'''
Use this script to integrate and store the following data (on backend)
from stackoverflow survey 2020 data:

- Work Industries (applications): array
- Developer Roles (career goals): array
- Correlated technologies (technologies): graph, adj matrix/list
'''

'''
"Career Goals" - developerRoles (role, percentage)
https://insights.stackoverflow.com/survey/2020#developer-profile-developer-type-all-respondents
'''
developerRoles = [
    ('Developer, back-end', 55.2),
    ('Developer, full-stack', 54.9),
    ('Developer, front-end', 37.1),
    ('Developer, desktop or enterprise applications', 23.9),
    ('Developer, mobile', 19.2),
    ('DevOps specialist', 12.1),
    ('Database administrator', 11.6),
    ('Designer', 10.8),
    ('System administrator', 10.6),
    ('Developer, embedded applications or devices', 9.6),
    ('Data or business analyst', 8.2),
    ('Data scientist or machine learning specialist', 8.1),
    ('Developer, QA or test', 8.0),
    ('Engineer, data', 7.6),
    ('Academic researcher', 7.2),
    ('Educator', 5.9),
    ('Developer, game or graphics', 5.6),
    ('Engineering manager', 5.5),
    ('Product manager', 5.1),
    ('Scientist', 4.2),
    ('Engineer, site reliability', 3.9),
    ('Senior executive/VP', 2.7),
    ('Marketing or sales professional', 1.3),
]

'''
"applications" - Work Industries (industry, percentage)
https://insights.stackoverflow.com/survey/2019#developer-roles
'''
Industries = [
    ('Software development - other', 11.9),
    ('Information technology', 10.9),
    ('Financial and banking', 8.9),
    ('Software as a service (saas) development', 7.6),
    ('Web development or design', 7.6),
    ('Consulting', 7.0),
    ('Data and analytics', 5.7),
    ('Health care or social services', 4.4),
    ('Media, advertising, publishing, or entertainment', 3.9),
    ('Retail or ecommerce', 3.8),
    ('Internet', 3.3),
    ('Education and training', 3.3),
    ('Manufacturing', 2.8),
    ('Cloud-based solutions or services', 2.8),
    ('Government or public administration', 2.7),
    ('Research - academic or scientific', 2.6),
    ('Telecommunications', 2.3),
    ('Transportation', 2.0),
    ('Energy or utilities', 1.8),
    ('Security', 1.4),
    ('Marketing', 1.3),
    ('Travel', 1.1),
    ('Nonprofit', 0.6),
    ('Real estate', 0.6)
]

'''
Correlated technologies graph

Select up to 5 technologies you are profficient in
Select up to 3 technologies you would like to learn

https://insights.stackoverflow.com/survey/2020#correlated-technologies
'''
