from flask import Blueprint, render_template , session
from requires import login_required
admin = Blueprint('admin', __name__)

@admin.route('/admin')
@login_required
def admin_func():
    return render_template('admin/admin.html')
