#!bin/bash
source venv/Scripts/activate

export FLASK_APP=webapp.py
export FLASK_ENV=development
flask run
