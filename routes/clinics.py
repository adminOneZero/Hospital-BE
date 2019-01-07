# -*- coding: utf-8 -*-
from flask import Blueprint, render_template , session , current_app
from requires import login_required
from db import Connection
clinics = Blueprint('clinics', __name__)

@clinics.route('/clinics')
@login_required
def clinics_func():
    # username = session['username']
    # cursor , conn = Connection()
    # q = """SELECT * FROM users WHERE username = '%s'""" %(username)
    # result = cursor.execute(q)
    # userInfo = cursor.fetchone()

    return render_template('admin/clinics.html')
