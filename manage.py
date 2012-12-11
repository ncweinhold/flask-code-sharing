from os.path import abspath

from flask import current_app
from flask.ext.script import Manager
from pasteapp import create_app
from pasteapp.database import init_db, clear_db

manager = Manager(create_app)
manager.add_option('-c', '--config', type=abspath, dest='cfg_file',
                   default='config_devel.py')

@manager.command
def initialise_db():
    with current_app.app_context():
        init_db()

@manager.command
def drop_db():
    with current_app.app_context():
        clear_db()

if __name__ == '__main__':
    manager.run()
