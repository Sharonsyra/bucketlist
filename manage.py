import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from config import ProductionConfig, StagingConfig, DevelopmentConfig, TestingConfig


from run import app, db
from models import User, BucketList, Item

app.config.from_object(DevelopmentConfig)

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()


if __name__ == '__main__':
    manager.run()
