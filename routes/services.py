# -*- coding: utf-8 -*-
from flask import Blueprint, render_template , session , current_app ,\
 jsonify, request
from requires import login_required
from db import Connection
from codecs import encode
from flask_paginate import Pagination, get_page_parameter
from lib import pagination
services = Blueprint('services', __name__)


@services.route('/services/')
@login_required
def services_home(offset = 1):
    inOnePage = current_app.config['resultsInOnePage'] # numbers of items in one page
    services = pagination(inOnePage,'Services') pagination object
    paginate = {}

    # get all services data as page number one
    cursor , conn = Connection() # open Connection to db
    q = """select * from Services LIMIT {0}""".format(inOnePage)
    result = cursor.execute(q)
    services_data = cursor.fetchall() # get all rows

    # numbers of pages or bottoms
    paginate['btn_num'] = services.paginate()
    if paginate['btn_num'] == [1] :
        paginate['show_btn'] = False
    else:
        paginate['show_btn'] = True

    paginate['back'] = 1
    paginate['next'] = 2


    # get all clinic to show them
    q = """select ar_name,en_name from ClinicList """ # get just limit rows
    result = cursor.execute(q)
    clinics = cursor.fetchall() # get all rows

    current_app.logger.info(paginate)

    return render_template('admin/services.html',services_data=services_data,paginate=paginate,clinics=clinics)


# services page with page parameters
@services.route('/services/<offset>')
@login_required
def services_func(offset = 1):
    # the nubers of services items we need in one page
    inOnePage = current_app.config['resultsInOnePage']
    services = pagination(inOnePage,'Services') # pagination object

    # handle ValueError if user giv us string
    try:
        offset = int(encode(offset, 'utf-8', 'strict'))
    except ValueError as e:
        offset = 1
    # paginate information for pagenation array object
    paginate = {}
    paginate['next'] = int(offset) + 1
    paginate['back'] = int(offset) - 1

    # if offset page of page that user is need equal one
    # set back and next bottoms to default
    if offset == 1 :
        paginate['back'] = 1
        paginate['next'] = 2

    # get numbers of bottoms or pages
    paginate['btn_num'] = services.paginate()
    paginate['show_btn'] = True # any way

    offset = services.offset(offset) # possion of page in db
    cursor , conn = Connection() # open Connection to db
    q = """SELECT * FROM Services LIMIT {0} OFFSET {1}""".format(inOnePage,offset)
    result = cursor.execute(q)
    services_data = cursor.fetchall()

    # get all clinic to show them as list
    q = """select ar_name,en_name from ClinicList """
    result = cursor.execute(q)
    clinics = cursor.fetchall() # fetch all rows

    return render_template('admin/services.html',services_data=services_data,paginate=paginate,clinics=clinics)



# add new service
@services.route('/api/services/add',methods=['POST'])
@login_required
def services_add():
    numbers = ['1','2','3','4','5','6','7','8','9','0']
    service_code  = request.form['service_code'].encode('utf8')
    ar_name       = request.form['ar_name'].encode('utf8')
    en_name       = request.form['en_name'].encode('utf8')
    service_cost  = request.form['service_cost'].encode('utf8')
    inner_clinic  = request.form['inner_clinic'].encode('utf8')

    if service_cost == '' and inner_clinic == '':
        return jsonify({'message':' اختر اما عياده خارجيه او داخليه '})

    # check if service code is a number
    check_service_id = [i for i in service_code + service_cost]
    for i in check_service_id:
        if i not in numbers or i == '':
            return jsonify({'message':' الرجاء ادخال كود الخدمه ','MSG_type':'danger'})
    if service_code == '':
        return jsonify({'message':' الرجاء ادخال كود الخدمه ','MSG_type':'danger'})

    # start connecion to db
    cursor , conn = Connection()
    # check is service code exists in db or not
    q = """Select serviceCode From Services WHERE serviceCode ='{0}' LIMIT 1""".format(service_code)
    result = cursor.execute(q)

    # if id not exists insert data
    if result == 0:
        q = """INSERT INTO Services (serviceCode,serviceAr,serviceEN,serviceCosting,clinic) VALUES ('{0}','{1}','{2}','{3}','{4}')""".format(service_code,ar_name,en_name,service_cost,inner_clinic)
        result = cursor.execute(q)
        conn.commit()
        return jsonify({'message':' تمت الاضافه بنجاح ','MSG_type':'success'})
    else :
        return jsonify({'message':' كود الخدمه موجود مسبقا ','MSG_type':'warning'})

    return jsonify({'message':' اعد تحميل الصفحه ','MSG_type':'danger'})


# get services data for editing
@services.route('/api/services/edit',methods=['POST'])
@login_required
def clinics_edit():
    service_id = request.form['service_id']
    # if service id is valid
    numbers = ['1','2','3','4','5','6','7','8','9','0']
    check_service_id = [i for i in service_id]
    for i in check_service_id:
        if i not in numbers:
            return jsonify({'message':' طلب غير صحيح ','MSG_type':'danger'})

    cursor , conn = Connection()
    q = """SELECT * FROM Services WHERE id = '{0}' """.format(service_id)
    result = cursor.execute(q)
    data = cursor.fetchone()
    # get clinics list to allow user change the service's slinic
    q = """select ar_name,en_name from ClinicList """
    result = cursor.execute(q)
    conn.commit()
    all_clinics = list(cursor.fetchall()) # get all rows

    service_data = {
    'service_id': data[0],
    'service_code': data[1],
    'ar_name': data[2],
    'en_name': data[3],
    'clinic': all_clinics,
    'service_costing': data[7]
    }
    return jsonify(service_data)


# update service data
@services.route('/api/services/update',methods=['POST'])
@login_required
def services_update():
    current_app.logger.info(list(request.form))

    service_code     = request.form['service_code'].encode('utf8')
    service_id       = request.form['service_id'].encode('utf8')
    en_name          = request.form['en_name'].encode('utf8')
    ar_name          = request.form['ar_name'].encode('utf8')
    service_cost     = request.form['service_cost'].encode('utf8')
    clinic          = request.form['clinic'].encode('utf8')
    # if id is valid as number
    numbers = ['1','2','3','4','5','6','7','8','9','0']
    check_service_id = [i for i in service_id + service_code + service_cost]
    for i in check_service_id:
        if i not in numbers:
            return jsonify({'message':' طلب غير صحيح ','MSG_type':'danger'})

    cursor , conn = Connection()
    # check is service code exists in db or not
    q = """SELECT serviceCode FROM Services WHERE id ='{0}' LIMIT 1""".format(service_id)
    result = cursor.execute(q)
    conn.commit()
    current_app.logger.info(result)
    # return jsonify({})
    if result == 1:
        q = """UPDATE Services SET serviceAR="{0}", serviceEN="{1}", serviceCode="{2}" , serviceCosting="{3}" , clinic="{4}" WHERE id = "{5}" """.format(ar_name,en_name,service_code,service_cost,clinic,service_id)
        result = cursor.execute(q)
        conn.commit()
        if result == 0:
            return jsonify({'message':' فشلت عمليه التعديل ','MSG_type':'danger'})
        else :
            return jsonify({'message':' تم تحديث بيانات الخدمه بنجاح ','MSG_type':'success'})
    else :
        return jsonify({'message':' كود الخدمه مضاف مسبقا ','MSG_type':'warning'})

# delete serice
@services.route('/api/services/delete',methods=['POST'])
@login_required
def service_delete():
    db_id = request.form['db_id'].encode('utf8')

    # if id is valid as number
    numbers = ['1','2','3','4','5','6','7','8','9','0']
    check_service_id = [i for i in db_id]
    for i in check_service_id:
        if i not in numbers:
            return jsonify({'message':' طلب غير صحيح ','MSG_type':'danger'})

    cursor , conn = Connection()
    q = """DELETE FROM Services WHERE id="{0}" """.format(db_id)
    result = cursor.execute(q)
    conn.commit()
    if result == 1:
        return jsonify({'message':' تم الحذف بنجاح ','MSG_type':'success'})
    return jsonify({'message':' لما يتم الحذف ','MSG_type':'danger'})



# search about clinics
@services.route('/api/services/search',methods=['POST','GET'])
@login_required
def clinics_search():
    search = request.form['search'].encode('utf8')
    if search == '':
        return jsonify({'message':' اكتب كلمه البحث ','MSG_type':'warning'})

    # if search keyword just a numbers then get search as service code
    search_keyword = [i for i in search]
    numbers = ['1','2','3','4','5','6','7','8','9','0']
    for i in search_keyword:
        if i not in numbers :
            break
        else:
            cursor , conn = Connection()
            # search into db
            q = """ SELECT * FROM Services WHERE serviceCode = {0}""".format(search)
            result = cursor.execute(q)
            row = cursor.fetchone()
            if result == 1: # if data found go and jsonify this data
                search_data = [{
                'db_id': data[0], # or service_id is same
                'service_code': data[1],
                'ar_name': data[2],
                'en_name': data[3],
                'clinic': all_clinics,
                'service_costing': data[3]
                }]
                return jsonify(search_data) # return all data founds

    cursor , conn = Connection()
    # search into db
    q = """ SELECT * FROM Services WHERE serviceAr LIKE '%{0}%' OR  serviceEN LIKE '%{0}%' OR  clinic LIKE '%{0}%' LIMIT 10""".format(search)
    result = cursor.execute(q)
    rows = cursor.fetchall() # get all data
    conn.commit()

    # get clinics list to allow user change the service's slinic
    q = """select ar_name,en_name from ClinicList """
    result = cursor.execute(q)
    conn.commit()
    all_clinics = list(cursor.fetchall()) # get all rows

    if result > 0: # if data found go and jsonify this data
        search_data = [] # append here all data as dictionarys
        for row in rows : # loop over rows
            # append to list this dictionary
            search_data.append({
            'db_id': row[0], # or ervice_id is same
            'service_code': row[1],
            'ar_name': row[2],
            'en_name': row[3],
            'clinic': row[6],
            'service_costing': row[7]
            })
        return jsonify(search_data) # return all data founds
    return jsonify({'message':' لاتوجد نتائج ','MSG_type':'warning'})
