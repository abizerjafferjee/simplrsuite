import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import config

from app import app, db

# app.config.from_object(config.Config)
if os.environ.get('FLASK_ENVIRONMENT') == 'PROD':
    app.config.from_object(config.ProductionConfig)
else:
    app.config.from_object(config.DevelopmentConfig)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
