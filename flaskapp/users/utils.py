# users/utils.py
import os
import secrets
from PIL import Image
from flask import url_for, current_app

def save_picture_helper(form_picture):
    ''' helper function which
    1) Takes pictures field (.jpg, .png) submitted on form
    2) Set save location for picures
    3) Resize and save image '''

    # creating unique name when saving pictures
    rand_hex = secrets.token_hex(nbytes=8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_filename = rand_hex + file_ext
    # Setting file path for save location
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_filename)

    # image resizing and saving
    output_size = (125, 125)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)

    return picture_filename
