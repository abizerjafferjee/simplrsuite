import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pw@localhost/thumbtack'
    SQLALCHEMY_DATABASE_URI = 'postgresql://simplr_suite:admin@localhost/simplr_suite'
    CSRF_ENABLED = True
    SECRET_KEY = '5S73gu33234qWSC1O2'
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 100, 'max_overflow':40, 'pool_recycle': 300}
    UPLOAD_FOLDER = '../vue-app/vue-app/src/assets/uploads' # the relative path to upload to

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://simplr_suite:admin@localhost/simplr_suite'

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pw@localhost/thumbtack'
    SQLALCHEMY_DATABASE_URI = 'postgresql://simplr_suite:admin@localhost/simplr_suite'
