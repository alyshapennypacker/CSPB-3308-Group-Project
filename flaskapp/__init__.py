from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskapp.config import Config


# Site Extensions: Keep outside of create_app, so 1 extention object can be used for many instances
db = SQLAlchemy()                                   # Database
bcrypter = Bcrypt()                                 # Password hashing
login_manager = LoginManager()                      # Configure login manager client sesions
login_manager.login_view = 'users.login' 
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    """
    Creates an instance of flask app
    """
    # Initialize app, init key to manage sessions
    app = Flask(__name__)
    # App using Config class values
    app.config.from_object(Config)

    # Instance extensions
    app.app_context().push()
    db.init_app(app)
    bcrypter.init_app(app)
    login_manager.init_app(app)

    # import routes from blueprint instances and register routes to App
    from flaskapp.users.routes import users
    from flaskapp.projects.routes import projects
    from flaskapp.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(projects)
    app.register_blueprint(main)

    return app