# -*- coding: utf-8 -*-
from flask import Blueprint, render_template , session , current_app ,\
 jsonify, request
from requires import login_required
from db import Connection
from codecs import encode
from flask_paginate import Pagination, get_page_parameter
from lib import pagination

clinics = Blueprint('clinics', __name__)


@clinics.route('/clinics/')
@login_required
def clinics_home(offset = 1):
    inOnePage = current_app.config['clinicsInOnePage'] # numbers of items in one page
    clinics = pagination(inOnePage,'ClinicList') # pagination object
    paginate = {}

    cursor , conn = Connection() # open Connection to db
    q = """select * from ClinicList LIMIT {0}""".format(inOnePage) # get just limit rows
    result = cursor.execute(q)
    clinic_data = cursor.fetchall() # get all rows


    paginate['btn_num'] = clinics.paginate()
    # current_app.logger.info(paginate['btn_num'])
    if paginate['btn_num'] == [1] :
        paginate['show_btn'] = True
    else:
        paginate['show_btn'] = False

    paginate['back'] = 1
    paginate['next'] = 2

    return render_template('admin/clinics.html',clinic_data=clinic_data,paginate=paginate)


# clinics page with page parameters
@clinics.route('/clinics/<offset>')
@login_required
def clinics_func(offset = 1):
    # the nubers of clinics items we need in one page
    inOnePage = current_app.config['clinicsInOnePage'] # numbers of items in one page
    clinics = pagination(inOnePage,'ClinicList') # pagination object
    paginate = {}

    try:
        offset = int(encode(offset, 'utf-8', 'strict'))
    except ValueError as e:
        offset = 1
    # paginate information for pagenation array object
    paginate = {}
    paginate['next'] = int(offset) + 1
    paginate['back'] = int(offset) - 1

    # if offset page of page that user is need equal one set back and next bottoms values
    if offset == 1 :
        paginate['back'] = 1
        paginate['next'] = 2

    # get clinics item for page what user need from page
    offset = clinics.offset(offset)
    cursor , conn = Connection() # open connection
    q = """SELECT * FROM ClinicList LIMIT {0} OFFSET {1}""".format(inOnePage,offset)
    result = cursor.execute(q)
    clinic_data = cursor.fetchall()

    # all pages in db as bottoms
    paginate['btn_num'] = clinics.paginate()
    if paginate['btn_num'] == [1] :
        paginate['show_btn'] = False
    else:
        paginate['show_btn'] = True

    return render_template('admin/clinics.html',clinic_data=clinic_data,paginate=paginate)



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
