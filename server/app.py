from flask import Flask, jsonify, request, render_template,make_response,session,redirect,url_for
from flask_cors import CORS
from datetime import datetime
from dbcon import dbmanager
from bson.json_util import dumps, loads
import pprint
import os
import ast

app = Flask(__name__)
CORS(app)
#app.secret_key = 'test_secret'
DEBUG = True
KEY = 'request_number'

def convertCursorToJson(_cursor) :
    lst = list()
    lst.append(_cursor)
    return dumps(lst)
def getNowTimeStr() :
    return (datetime.now()).strftime("%d/%m/%Y %H:%M:%S")


@app.route('/dodotest')
def init_page():
    return render_template('test_back_page.html')

"""
Request data
"""
@app.route('/api/request', methods=['POST','GET'])
def serve_request_data():
    dbManager = dbmanager.MongoDbManager('user_requests')
    if request.method == 'POST':
        mode_received = request.form['mode']
        ### ADD data ###
        if mode_received == "add": 
            id_received = request.form['key']
            ipaddr_received = request.remote_addr
            now_time = getNowTimeStr()
            #f = request.files['file']
            result = dbManager.add_data({
                            KEY : id_received , 
                            'ip': ipaddr_received,
                            'time' : now_time,
                            #'file' : f.filename
                            })
            if result != False :
                return jsonify({'result': 'success', 
                                'work': 'add data to DB', 
                                'user_id': id_received})
            else :
                return jsonify({'result': 'fail', 
                                'work': 'add data to DB', 
                                'user_id':id_received})
        ### DELETE data ###
        elif mode_received=="delete" : 
            query = { KEY : request.form['key']}
            result = dbManager.del_data(query)
            if result != False :
                return jsonify({'result': 'success', 
                                'work': 'delete data from DB', 
                                'input':query})
            else : 
                return jsonify({'result': 'fail', 
                                'work': 'delete data from DB', 
                                'input':query})
    #Get data from DB
    elif request.method == 'GET':
        query_received = request.args.get('query')            
        query = ast.literal_eval(query_received)
        data = dbManager.get_data(query)
        return convertCursorToJson(data)
    

"""
Result data
"""
@app.route('/api/result', methods=['POST','GET'])
def serve_result_data():
    dbManager = dbmanager.MongoDbManager('analyze_result')
    if request.method == 'POST':
        mode_received = request.form['mode']
        ### ADD data ###
        if mode_received == "add": 
            id_received = request.form['key']
            now_time = getNowTimeStr()
            #f = request.files['file']
            result = dbManager.add_data({
                            KEY : id_received , 
                            'time' : now_time,
                            'resultdata': 'testtesttest'
                            #'file' : f.filename
                            })
            if result != False :
                return jsonify({'result': 'success', 
                                'work': 'add data to DB', 
                                'user_id': id_received})
            else :
                return jsonify({'result': 'fail', 
                                'work': 'add data to DB', 
                                'user_id':id_received})
        ### DELETE data ###
        elif mode_received=="delete" : 
            query = { KEY : request.form['key']}
            result = dbManager.del_data(query)
            if result != False :
                return jsonify({'result': 'success', 
                                'work': 'delete data from DB', 
                                'input':query})
            else : 
                return jsonify({'result': 'fail', 
                                'work': 'delete data from DB', 
                                'input':query})
    #Get data from DB
    elif request.method == 'GET':
        query_received = request.args.get('query')            
        query = ast.literal_eval(query_received)
        data = dbManager.get_data(query)
        return convertCursorToJson(data)


# @app.route('/test_back_page/fileUpload', methods = ['GET','POST'])
# def upload_file():
#     if request.method == 'POST':
#         try:
#             client = MongoClient(host='localhost', port=27017)
#             db = client['mytest']['myCol']  
#             print("mongo connected:")
#             print(db)
#             ip_address = request.remote_addr
#             now = datetime.now()
#             now_time = now.strftime("%d/%m/%Y %H:%M:%S")
            
#             f = request.files['file']
#             if (f.filename).endswith('.csv') :
#                 print ("this is csv")
#             else : print("check out input file format")

#             sFilename = secure_filename(f.filename)
#             f.save("./uploads/"+sFilename)
            
#             submit_info = {'session_ip': ip_address, 
#                            'access_time':now_time,
#                            'file_name': sFilename
#                         }
#             print(submit_info)
#             x = db.insert_one(submit_info)
#             #flash("파일 업로드 완료")
#         except :
#             print("mongo connection fail")
#         finally: 
#             client.close()
#     return redirect(url_for('render_page'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3050, debug=True)
