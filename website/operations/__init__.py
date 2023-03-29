# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 - present Felix Abascal
"""

from flask import Blueprint

blueprint = Blueprint(
    'settings_blueprint',
    __name__,
    url_prefix=''
)