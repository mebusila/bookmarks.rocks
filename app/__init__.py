# -*- coding: utf-8 -*-
"""
    bookmarks.rocks.app
    ~~~~~~~~~~~~~~~~~~~

"""
__author__ = 'Serban Carlogea'

from flask import Flask
from flask.ext.mongoengine import MongoEngine
from config import config

db = MongoEngine()


def create_app(config_name):
    """Setup the application an `Application Factory <http://flask.pocoo.org/docs/0.10/patterns/appfactories/>`_

    .. todo:: Create blueprints from each modules from resources package

    :param config_name: Name of configuration to load
    :return: An instance of :class:`~flask.Flask`
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config.from_envvar('BR_LOCAL_CONFIG', silent=True)
    app.log = app.logger

    if not app.config['DEBUG'] and not app.config['TESTING']:
        # email errors to the administrators
        if app.config.get('MAIL_ERROR_RECIPIENT') is not None:
            import logging
            from logging.handlers import SMTPHandler
            credentials = None
            secure = None
            if app.config.get('MAIL_USERNAME') is not None:
                credentials = (app.config['MAIL_USERNAME'],
                               app.config['MAIL_PASSWORD'])
                if app.config['MAIL_USE_TLS'] is not None:
                    secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr=app.config['MAIL_DEFAULT_SENDER'],
                toaddrs=[app.config['MAIL_ERROR_RECIPIENT']],
                subject='[Bookmarks rocks] Application Error',
                credentials=credentials,
                secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        # send standard logs to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(app.config['LOG_LEVEL'])
        app.logger.addHandler(syslog_handler)

    db.init_app(app)

    from .resources import resources as resources_blueprint
    app.register_blueprint(resources_blueprint)

    return app
