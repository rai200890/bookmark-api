from bookmark_api import app, db
from bookmark_api.models import User

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def create_user(username, password):
    try:
        if User.query.filter_by(username=username).first() is not None:
            raise ValueError('User already exists')
        user = User(username=username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        app.logger.success('User created successfully')
    except Exception as e:
        app.logger.error(e)


if __name__ == "__main__":
    manager.run()
