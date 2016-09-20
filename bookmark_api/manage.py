from flask_script import Manager

from bookmark_api import app, db, models

manager = Manager(app)

@manager.command
def create_tables():
    db.create_all()
    db.session.commit()

if __name__ == "__main__":
    manager.run()
