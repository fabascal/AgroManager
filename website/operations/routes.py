# -*- encoding: utf-8 -*-
"""
Copyright (c) 2023 - present Felix Abascal
"""

from website.operations import blueprint
from website.operations.models import Predio
from website.authentication.models import Usuario
from flask import jsonify, make_response

@blueprint.route('/predios', methods=['GET','PUT'])
def predios():
    predios = Usuario.query.all()
    print(predios)
    return jsonify(predios[0])