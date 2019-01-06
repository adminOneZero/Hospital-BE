# -*- coding: utf-8 -*-
from flask import Blueprint, session , jsonify
from requires import backend_flash
flash = Blueprint(None,__name__)

@flash.route('/flash')
@backend_flash # check flash session is set or not to set
def get_flash():
    message = []
    if session['flash'] > 0:
        message = session['flash']
        session['flash'] = []
    return jsonify(message)
