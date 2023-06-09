# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present Felix Abascal
"""

import os
from decouple import config

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default='65fS#perS3crEt_007as5')

    # This will create a file in <app> FOLDER
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'AgroMananager.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SCHEDULER_API_ENABLED = True



class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config('DB_ENGINE', default='postgresql'),
        config('DB_USERNAME', default='flask'),
        config('DB_PASS', default='python-postgres'),
        config('DB_HOST', default='localhost'),
        config('DB_PORT', default=5432),
        config('DB_NAME', default='VisorVolumetrico')
    )


class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}