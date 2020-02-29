import os
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from propertySys import create_app, db

app = create_app('default')

migrate = Migrate(app, db, render_as_batch=True)
manager = Manager(app)

def make_shell_context():
  """自动加载环境"""
  return dict(
      app = app,
      db = db,
      )
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
