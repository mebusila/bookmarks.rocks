# -*- coding: utf-8 -*-
import os
import json
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Main configuration class
    Options here can be overwritten by child configuration.
    Configuration options can also be overwritten by setting the
    :envvar:`BR_LOCAL_CONFIG` envinronment variable to a configuration file.

    """
    #: Secret key
    SECRET_KEY = os.environ.get('SECRET_KEY')
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY')

    #: Root PATH of deployment
    #: All application PATHs should be relative to this
    ROOT = os.path.dirname(os.path.abspath(__file__))

    #: Enable debugging
    DEBUG = True

    MONGODB_DB = 'bookmarks'

    #: Email server
    MAIL_SERVER = '127.0.0.1'
    #: Email port
    MAIL_PORT = 465
    #: Use TLS
    MAIL_USE_TLS = True
    #: Use SSL
    MAIL_USE_SSL = False
    #: E-mail username
    MAIL_USERNAME = 'username'
    #: E-mail password
    MAIL_PASSWORD = 'mailpass'
    MAIL_DEFAULT_SENDER = 'some@mail.com'


class DevelConfig(Config):
    DEBUG = True
    SECRET_KEY = 'yXQ3MvrftJAPmupURUAN3PjM'
    WTF_CSRF_SECRET_KEY = 'XH#I912[W9[Rm$4JYtv7Urb@sdfc38cm6'


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    WTF_CSRF_ENABLED = False
    TESTS = os.path.join(Config.ROOT, 'tests')


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    JSON_AS_ASCII = False
    CSRF_ENABLED = True

config = {
    'devel': DevelConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelConfig
}
