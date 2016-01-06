#!venv/bin/python
# -*- coding: utf-8 -*-
"""
    Application manager
    ~~~~~~~~~~~~~~~~~~

    Add basic command line actions for the application.
    Similar to Django's manage.py
"""
import os
from flask.ext.script import Manager
from app import create_app
from app import models, db


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


@manager.shell
def make_shell_content():
    return dict(app=app, db=db, models=models)


if __name__ == '__main__':
    manager.run()
