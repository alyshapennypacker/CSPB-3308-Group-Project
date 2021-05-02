from flask import render_template, request, Blueprint
from flaskapp.models import Projects


main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    projects = Projects.query.all()
    projects = sorted(projects, key=lambda x: x.creation_timestamp, reverse=True)
    for project in projects:
        print(project.creation_timestamp)
    return render_template('home.html', projects=projects)


@main.route('/about')
def about():
    return render_template('about.html')
