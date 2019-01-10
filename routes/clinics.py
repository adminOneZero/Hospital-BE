# -*- coding: utf-8 -*-
from flask import Blueprint, render_template , session , current_app ,\
 jsonify, request
from requires import login_required
from db import Connection
clinics = Blueprint('clinics', __name__)

@clinics.route('/clinics')
@login_required
def clinics_func():
    cursor , conn = Connection()
    q = """SELECT * FROM ClinicList """
    result = cursor.execute(q)
    clinic_data = cursor.fetchall()
    return render_template('admin/clinics.html',clinic_data=clinic_data)


@clinics.route('/api/clinics',methods=['POST'])
@login_required
def clinics_post():
    numbers = ['1','2','3','4','5','6','7','8','9','0']
    clinic_id = request.form['clinic_id'].encode('utf8')
    ar_name   = request.form['ar_name'].encode('utf8')
    en_name   = request.form['en_name'].encode('utf8')
    username  = session['username'].encode('utf8')

    # check if clinic is a number
    check_clinic_id = [i for i in clinic_id]
    for i in check_clinic_id:
        # for num not in numbers:
        if i not in numbers or i == '':
            return jsonify({'message':' الرجاء ادخال رقم العياده/جهه ','MSG_type':'danger'})
    if clinic_id == '':
        return jsonify({'message':' الرجاء ادخال رقم العياده/جهه ','MSG_type':'danger'})

    # start connecion to db
    cursor , conn = Connection()
    # check is clinic id exists in db or not
    q = """Select clinic_id From ClinicList WHERE clinic_id ='{0}' LIMIT 1""".format(clinic_id)
    result = cursor.execute(q)
    # if id not exists insert data
    if result == 0:
        q = """INSERT INTO ClinicList (username,clinic_id,ar_name,en_name) VALUES ('{0}','{1}','{2}','{3}')""".format(username,clinic_id,ar_name,en_name)
        result = cursor.execute(q)
        conn.commit()
        return jsonify({'message':' تمت الاضافه بنجاح ','MSG_type':'success'})
    else :
        return jsonify({'message':' رقم العياده او الجهه مضافه مسبقا ','MSG_type':'warning'})

    return jsonify({'message':' اعد تحميل الصفحه ','MSG_type':'danger'})
