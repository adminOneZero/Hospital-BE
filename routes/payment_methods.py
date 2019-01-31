# -*- coding: utf-8 -*-
from flask import Blueprint, render_template , session , current_app ,\
 jsonify, request
from requires import login_required
from db import Connection
from codecs import encode
payment_methods = Blueprint('payment_methods', __name__)


@payment_methods.route('/payment_methods/')
@login_required
def payment_methods_home():
    return render_template('admin/payment_methods.html')
