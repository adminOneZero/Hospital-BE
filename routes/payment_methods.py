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
    inOnePage = current_app.config['paymentInOnePage'] # numbers of items in one page
    # start connecion to db
    cursor , conn = Connection()
    q = """select * from payment_methods LIMIT {0}""".format(inOnePage) # get just limit rows
    result = cursor.execute(q)
    payment_data = cursor.fetchall()

    conn.commit()

    return render_template('admin/payment_methods.html',payment_data=payment_data)


# add new clinic
@payment_methods.route('/api/payment_methods/add',methods=['POST'])
@login_required
def payment_methods_add():
    numbers          = ['1','2','3','4','5','6','7','8','9','0']
    ar_name          = request.form['ar_name'].encode('utf8')
    en_name          = request.form['en_name'].encode('utf8')
    payment_method   = request.form['payment'].encode('utf8')
    discount_value   = request.form['discount_value'].encode('utf8')
    discount_type    = request.form['discount_type'].encode('utf8')

    current_app.logger.info(request.form)
    # return 'yes'
    # check if clinic is a number
    check_is_numbers = [i for i in str(discount_value)]
    for i in check_is_numbers:
        # for num not in numbers:
        if i not in numbers or i == '':
            return jsonify({'message':' مدخلات غير صحيحه ','MSG_type':'danger'})
    if  discount_value  == '' or discount_type == '' or ar_name == '' or en_name == '' or payment_method == '' :
        return jsonify({'message':' مدخلات غير صحيحه ','MSG_type':'danger'})

    # start connecion to db
    cursor , conn = Connection()

    q = """INSERT INTO payment_methods (methods,ar_name,en_name,discount_type,discount_value) VALUES ('{0}','{1}','{2}','{3}','{4}') """.format(payment_method,ar_name,en_name,discount_type,discount_value)
    result = cursor.execute(q)
    conn.commit()
    if result == 1:
        return jsonify({'message':' تمت الاضافه بنجاح ','MSG_type':'success'})
    else:
        return jsonify({'message':' فشلت الاضافه ','MSG_type':'warning'})
