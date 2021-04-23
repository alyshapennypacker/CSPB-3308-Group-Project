from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Initialize app, init key to manage sessions
app = Flask(__name__)
app.config['SECRET_KEY'] = '46d19a02745253668092defebbb0b196'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Supress deprecation message

# Site Extensions:
db = SQLAlchemy(app)
bcrypter = Bcrypt(app) # Password hashing algo
login_manager = LoginManager(app) # Manages client sesions
login_manager.login_view, login_manager.login_message_category= 'login', 'info'

from flaskapp import routes # Import routes last to avoid 404 errors
