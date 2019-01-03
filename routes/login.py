from flask import Blueprint, render_template , session
from requires import logout_required
login = Blueprint('login', __name__)

@login.route('/login')
@logout_required
def login_func():
    return render_template('login/login.html')
