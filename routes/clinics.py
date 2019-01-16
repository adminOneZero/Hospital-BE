# -*- coding: utf-8 -*-
from flask import Blueprint, render_template , session , current_app ,\
 jsonify, request
from requires import login_required
from db import Connection
clinics = Blueprint('clinics', __name__)

# clinics page
@clinics.route('/clinics')
@login_required
def clinics_func():
    cursor , conn = Connection()
    q = """SELECT * FROM ClinicList """
    result = cursor.execute(q)
    clinic_data = cursor.fetchall()
    return render_template('admin/clinics.html',clinic_data=clinic_data)

# add new clinic
@clinics.route('/api/clinics/add',methods=['POST'])
@login_required
def clinics_add():
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


# get clinic data for editing
@clinics.route('/api/clinics/edit',methods=['POST'])
@login_required
def clinics_edit():
    clinic_id = request.form['clinic_id']
    # if clinic id is valid
    numbers = ['1','2','3','4','5','6','7','8','9','0']
    check_clinic_id = [i for i in clinic_id]
    for i in check_clinic_id:
        if i not in numbers:
            return jsonify({'message':' طلب غير صحيح ','MSG_type':'danger'})

    cursor , conn = Connection()
    q = """SELECT * FROM ClinicList WHERE id = '{0}' """.format(clinic_id)
    result = cursor.execute(q)
    data = cursor.fetchone()
    clinic_data = {
    'id': data[0],
    'clinic_id': data[1],
    'ar_name': data[2],
    'en_name': data[3]
    }
    return jsonify(clinic_data)

# update clinic data
@clinics.route('/api/clinics/update',methods=['POST'])
@login_required
def clinics_update():
    db_id = request.form['db_id'].encode('utf8')
    # current_app.logger.info(db_id)
    clinic_id = request.form['clinic_id'].encode('utf8')
    ar_name = request.form['ar_name'].encode('utf8')
    en_name = request.form['en_name'].encode('utf8')
    # if id is valid
    numbers = ['1','2','3','4','5','6','7','8','9','0']
    check_clinic_id = [i for i in clinic_id]
    for i in check_clinic_id:
        if i not in numbers:
            return jsonify({'message':' طلب غير صحيح ','MSG_type':'danger'})

    cursor , conn = Connection()
    # check is clinic id exists in db or not
    q = """SELECT clinic_id FROM ClinicList WHERE clinic_id ='{0}' LIMIT 1""".format(clinic_id)
    result = cursor.execute(q)
    conn.commit()
    if result == 0:
        q = """UPDATE ClinicList SET ar_name="{0}", en_name="{1}", clinic_id="{2}" WHERE id = "{3}" """.format(ar_name,en_name,clinic_id,db_id)
        result = cursor.execute(q)
        conn.commit()
        if result == 0:
            return jsonify({'message':' فشل تحديث البيانات ','MSG_type':'danger'})
        else :
            return jsonify({'message':' تم تحديث بيانات العياده/الجهه بنجاح ','MSG_type':'success'})
    else :
        return jsonify({'message':' رقم العياده او الجهه مضافه مسبقا ','MSG_type':'warning'})


# delete clinics
@clinics.route('/api/clinics/delete',methods=['POST'])
@login_required
def clinics_delete():
    db_id = request.form['db_id'].encode('utf8')
    cursor , conn = Connection()
    q = """DELETE FROM ClinicList WHERE id="{0}" """.format(db_id)
    result = cursor.execute(q)
    conn.commit()
    if result == 1:
        return jsonify({'message':' تم الحذف بنجاح ','MSG_type':'success'})
    return jsonify({'message':' لما يتم الحذف ','MSG_type':'danger'})


# search about clinics
@clinics.route('/api/clinics/search',methods=['POST','GET'])
@login_required
def clinics_search():
    search = request.form['search'].encode('utf8')
    if search == '':
        return jsonify({'message':' اكتب كلمه البحث ','MSG_type':'warning'})

    # if search keyword just a numbers get clinic id fro db
    search_keyword = [i for i in search]
    numbers = ['1','2','3','4','5','6','7','8','9','0']
    for i in search_keyword:
        if i not in numbers :
            break
        else:
            cursor , conn = Connection()
            # search into db
            q = """ SELECT * FROM ClinicList WHERE clinic_id = {0}""".format(search)
            result = cursor.execute(q)
            row = cursor.fetchone()
            if result == 1: # if data found go and jsonify this data
                search_data = [{
                'db_id': row[0],
                'clinic_id': row[1],
                'ar_name': row[2],
                'en_name': row[3]
                }]
                return jsonify(search_data) # return all data founds

    cursor , conn = Connection()
    # search into db
    q = """ SELECT * FROM ClinicList WHERE en_name LIKE '%{0}%' OR  ar_name LIKE '%{0}%' LIMIT 10""".format(search)
    result = cursor.execute(q)
    rows = cursor.fetchall() # get all data
    conn.commit()

    if result > 0: # if data found go and jsonify this data
        search_data = [] # append here all data as dictionarys
        for row in rows : # loop over rows
            # append to list this dictionary
            search_data.append( {
            'db_id': row[0],
            'clinic_id': row[1],
            'ar_name': row[2],
            'en_name': row[3]
            })
        return jsonify(search_data) # return all data founds
    return jsonify({'message':' لاتوجد نتائج ','MSG_type':'warning'})
