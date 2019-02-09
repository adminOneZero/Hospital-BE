# -*- coding: utf-8 -*-
from flask import Blueprint, render_template , session , current_app ,\
 jsonify, request
from requires import login_required
from db import Connection
from codecs import encode
from lib import pagination
payment_methods = Blueprint('payment_methods', __name__)


@payment_methods.route('/payment_methods/')
@login_required
def payment_methods_home():
    inOnePage = current_app.config['paymentInOnePage'] # numbers of items in one page
    paymentMethods = pagination(inOnePage,'payment_methods') # pagination object

    # start connecion to db
    cursor , conn = Connection()
    q = """select * from payment_methods LIMIT {0}""".format(inOnePage) # get just limit rows
    result = cursor.execute(q)
    payment_data = cursor.fetchall()
    conn.commit()

    paginate = {}
    paginate['btn_num'] = paymentMethods.paginate()
    if paginate['btn_num'] == [1] :
        paginate['show_btn'] = True
    else:
        paginate['show_btn'] = False

    paginate['back'] = 1
    paginate['next'] = 2

    return render_template('admin/payment_methods.html',payment_data=payment_data,paginate=paginate)


@payment_methods.route('/payment_methods/<offset>')
@login_required
def payment_methods_func(offset):
    inOnePage = current_app.config['paymentInOnePage'] # numbers of items in one page
    paymentMethods = pagination(inOnePage,'payment_methods') # pagination object

    try:
        offset = int(encode(offset, 'utf-8', 'strict'))
    except ValueError as e:
        offset = 1

    paginate = {}
    # all pages in db as bottoms
    paginate['btn_num'] = paymentMethods.paginate()
    paginate['next'] = int(offset) + 1
    paginate['back'] = int(offset) - 1
    if offset == 1 :
        paginate['back'] = 1
        paginate['next'] = 2

    offset = paymentMethods.offset(offset)
    # start connecion to db
    cursor , conn = Connection()
    q = """SELECT * FROM payment_methods LIMIT {0} OFFSET {1}""".format(inOnePage,offset) # get just limit rows
    result = cursor.execute(q)
    payment_data = cursor.fetchall()
    conn.commit()

    return render_template('admin/payment_methods.html',payment_data=payment_data,paginate=paginate)


# add new payment method
@payment_methods.route('/api/payment_methods/add',methods=['POST'])
@login_required
def payment_methods_add():
    numbers          = ['1','2','3','4','5','6','7','8','9','0']
    ar_name          = request.form['ar_name'].encode('utf8')
    en_name          = request.form['en_name'].encode('utf8')
    payment_method   = request.form['payment'].encode('utf8')
    discount_value   = request.form['discount_value'].encode('utf8')
    discount_type    = request.form['discount_type'].encode('utf8')

    # check if payment methods input is a number
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


# delete payment method
@payment_methods.route('/api/payment_methods/delete',methods=['POST'])
@login_required
def payment_methods_delete():
    db_id = request.form['db_id'].encode('utf8')

    # if id is valid as number
    numbers = ['1','2','3','4','5','6','7','8','9','0']
    check_payment_id = [i for i in db_id]
    for i in check_payment_id:
        if i not in numbers:
            return jsonify({'message':' طلب غير صحيح ','MSG_type':'danger'})

    cursor , conn = Connection()
    q = """DELETE FROM payment_methods WHERE id="{0}" """.format(db_id)
    result = cursor.execute(q)
    conn.commit()
    if result == 1:
        return jsonify({'message':' تم الحذف بنجاح ','MSG_type':'success'})
    return jsonify({'message':' لم يتم الحذق بنجاح ','MSG_type':'danger'})
