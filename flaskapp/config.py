''' Store App's configurations in a file

This Converts the creation of App to a function, so we can create instances of our app with different configurations
- to unpack our config obj -> app.config.from_object(Config) 
'''

import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Supress deprecation message