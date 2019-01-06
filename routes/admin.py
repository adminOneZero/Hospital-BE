# -*- coding: utf-8 -*-
from flask import Blueprint, render_template , session , current_app
from requires import login_required
from db import Connection
admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
def admin_func():
    username = session['username']
    cursor , conn = Connection()
    q = """SELECT * FROM users WHERE username = '%s'""" %(username)
    result = cursor.execute(q)
    userInfo = cursor.fetchone()
    return render_template('admin/info.html',userInfo=userInfo)
