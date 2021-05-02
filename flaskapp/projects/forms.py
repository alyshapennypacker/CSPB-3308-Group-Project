from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired
from flaskapp.models import Users, Languages, Careers


class ProjectForm(FlaskForm):
    """ Project creation """
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])

    choices_languages = [(row.id, row.name) for row in Languages.query.all()]
    languages = SelectMultipleField(u'Top programming languages in project', choices=choices_languages, coerce=int)

    choices_careers = [(row.id, row.name) for row in Careers.query.all()]
    careers_field = SelectMultipleField(u'Project members developer types', choices=choices_careers, coerce=int)

    submit = SubmitField('Post')
