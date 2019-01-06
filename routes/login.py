# -*- coding: utf-8 -*-
from flask import Blueprint, render_template , session ,current_app , request \
                  , jsonify
from requires import logout_required ,login_required , backend_flash
from db import Connection
login = Blueprint('login', __name__)

@login.route('/login')
@backend_flash # check flash session is set or not to set
@logout_required
def login_func():
    return render_template('login/login.html')

@login.route('/logout')
@login_required
def logoute():
    session['logged_in'] = None
    session['level'] = None
    session['username'] = None
    session['flash'] += [' لقد خرجت من النظام ']

    return render_template('login/login.html')

@login.route('/api/login',methods=['POST'])
@logout_required
def api_login():
    current_app.logger.info(request.form)
    username = request.form['username']
    password = request.form['password']

    cursor , conn = Connection()
    result = cursor.execute("SELECT * FROM users WHERE username = '%s'" %(username))
    if result > 0:
        from hashlib import sha512
        hash = sha512(password.encode('utf8'))
        hash = hash.hexdigest()    # return render_template('login/ax.html')

        row = cursor.fetchone()
        if row[3] == username and row[4] == hash:
            session['logged_in'] = True
            session['level'] = row[6]
            session['username'] = username

            current_app.logger.info(cursor.fetchone())
            response = jsonify({
                    'redirect' : 'yes',
                    'message' : ' مرحبا بك ',
                    'MSG_type' : 'success'
                            })
            return response

    return jsonify({
                    'redirect' : 'no',
                    'message' : ' اسم المستخدم او كلمه المرور غير صحيحه ',
                    'MSG_type' : 'danger'
                    })
