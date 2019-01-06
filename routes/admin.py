# -*- coding: utf-8 -*-

from flask import Blueprint, render_template , session , current_app
from requires import login_required
admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
def admin_func():
    return render_template('admin/info.html')
