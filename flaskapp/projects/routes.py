from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flaskapp import db
from flaskapp.models import Users, Languages, Careers, Projects
from flaskapp.projects.forms import ProjectForm


projects = Blueprint('projects', __name__)


@projects.route("/projects/new", methods=['GET', 'POST'])
@login_required
def new_project():
    form = ProjectForm()
    if form.validate_on_submit() and request.method == 'POST':
        new_project = Projects(name=form.title.data, desc=form.content.data, owner=current_user)
        db.session.add(new_project)
        db.session.commit()

        # Adding Multiple languages to a project
        for language in form.languages.data:
            project_language = Languages.query.filter_by(id=language).first()
            new_project.languages.append(project_language)

        # Adding Multiple Careers to a project
        for career in form.careers_field.data:
            project_career = Careers.query.filter_by(id=career).first()
            new_project.careers.append(project_career)

        new_project.members.append(current_user)
        db.session.commit()

        flash("Your post has been created successfully!", "success")
        return redirect(url_for('main.home'))
    return render_template('create_project.html', legend='New Project', form=form)


@projects.route("/projects/<int:project_id>")
def project(project_id):
    current_project = Projects.query.get_or_404(project_id)
    return render_template('project.html', title=current_project.name, current_project=current_project)


@projects.route("/projects/<int:project_id>/update", methods=['GET', 'POST'])
@login_required
def update_project(project_id):
    ''' Form for current user to update their project
    current user muster be owner of the posted project, otherwise 403 '''
    current_project = Projects.query.get_or_404(project_id)
    if current_project.owner != current_user:
        abort(403)

    form = ProjectForm()
    if form.validate_on_submit() and request.method == 'POST':
        current_project.name = form.title.data
        current_project.desc = form.content.data

        # Reset exising skills, so User inputs overrides existing values
        current_project.languages = []
        current_project.careers = []
        db.session.commit()

        for language in form.languages.data:
            project_language = Languages.query.filter_by(id=language).first()
            if project_language not in current_project.languages:
                current_project.languages.append(project_language)

        for career in form.careers_field.data:
            project_career = Careers.query.filter_by(id=career).first()
            current_project.careers.append(project_career)
        db.session.commit()

        flash('Your post has been updated!', 'success')
        return redirect(url_for('projects.project', project_id=current_project.id))

    elif request.method == 'GET':
        form.title.data = current_project.name
        form.content.data = current_project.desc

    return render_template('create_project.html', title='Update Project', form=form, legend='Update Project')


@projects.route("/projects/<int:project_id>/delete", methods=['POST'])
@login_required
def delete_project(project_id):
    current_project = Projects.query.get_or_404(project_id)
    if current_project.owner != current_user:
        abort(403)
    db.session.delete(current_project)
    db.session.commit()
    flash('Your project has been deleted!', 'success')
    return redirect(url_for('main.home'))


@projects.route("/projects/<int:project_id>/join", methods=['GET', 'POST'])
@login_required
def join_project(project_id):
    current_project = Projects.query.get_or_404(project_id)
    current_project.members.append(current_user)
    db.session.commit()
    flash('You succesfully joined the project!', 'success')
    return redirect(url_for('projects.project', project_id=project_id))


@projects.route("/projects/<int:project_id>/leave", methods=['GET', 'POST'])
@login_required
def leave_project(project_id):
    current_project = Projects.query.get_or_404(project_id)
    current_project.members.remove(current_user)
    db.session.commit()
    flash('You succesfully left the project!', 'success')
    return redirect(url_for('projects.project', project_id=project_id))
