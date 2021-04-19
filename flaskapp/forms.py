# source: https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog/03-Forms-and-Validation

'''Define fieldset, required and

'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp
import email_validator

# supported formats {first.last@Colorado.edu, identikey@colorad.edu}
coloradoEmail_regex = "(?:\w+\.\w+|\w{4}\d{4})@colorado\.edu"


class RegistrationForm(FlaskForm):
    """ RegistrationForm's Fields
    POSTS into Users table
    """
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=5, max=15)]
                           )

    # 2-layer regex email validation: standard via Email() + regexp @colorado.edu
    email = StringField('Email',
                        default="first.last@colorado.edu",
                        validators=[DataRequired(), Email(),
                                    validators.Regexp(coloradoEmail_regex)]
                        )

    password = PasswordField('Password',
                             validators=[DataRequired()]
                             )
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')]
                                     )
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    """ LoginForm's Fields

    """
    email = StringField('Email',
                        validators=[DataRequired(), Email(),
                                    validators.Regexp(coloradoEmail_regex)]
                        )
    password = PasswordField('Password',
                             validators=[DataRequired()]
                             )
    submit = SubmitField('Login')
    #
    remember = BooleanField('Remember Me')
