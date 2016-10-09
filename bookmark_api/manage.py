from bookmark_api import app, db
from bookmark_api.models import User, Role

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def create_roles():
    try:
        for name in ["admin", "client"]:
            role = Role(name=name)
            db.session.add(role)
        db.session.commit()
        app.logger.info('Roles created successfully')
    except Exception as e:
        app.logger.error(e)


@manager.command
def create_admin(username, password, email):
    try:
        user = User(username=username, email=email, role=Role.query.filter_by(name='admin').one())
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        app.logger.info('User created successfully')
    except Exception as e:
        app.logger.error(e)


if __name__ == "__main__":
    manager.run()
