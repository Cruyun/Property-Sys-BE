import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import app, db

migrate = Migrate(app, db, render_as_batch=True)
manager = Manager(app)

manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()i
