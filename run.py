# -*- coding: utf-8 -*-
from flask import Flask , render_template , session ,jsonify , request
from routes.admin import admin
from routes.login import login
from routes.flash import flash
from routes.clinics import clinics

app = Flask(__name__)
app.register_blueprint(admin)
app.register_blueprint(login)
app.register_blueprint(flash)
app.register_blueprint(clinics)

app.config['SECRET_KEY'] = '915a2b304e26d134bebddfae78d1ac6542e87436c64d3d7e2e4e89fef206041052f295fb96284d08daffe81e511a64d024f087b562e802468d48677638e893ae' # you need secret key to to create sessions and cookies do not share this

@app.route('/test')
def test_func():
    return render_template('test.html')


# 404 error
@app.errorhandler(404) #
def page_not_found(e):
    return render_template('error/404.html')

# 500 error
@app.errorhandler(500) #
def serner_error(e):
    if request.method == 'POST':
        return jsonify({'message':' فشل ','MSG_type':'dander'})


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
