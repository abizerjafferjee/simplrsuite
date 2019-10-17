import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Qsaxzop15@localhost/thumbtack'
    UPLOAD_FOLDER = '../vue-app/vue-app/src/assets/uploads'

