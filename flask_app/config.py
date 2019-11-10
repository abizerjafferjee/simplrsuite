import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '5S73gu33234qWSC1O2'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Qsaxzop15@localhost/thumbtack'
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 100, 'max_overflow':40, 'pool_recycle': 300}
    UPLOAD_FOLDER = '../vue-app/vue-app/src/assets/uploads'


