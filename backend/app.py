from flask import Flask, jsonify, request, render_template,make_response,session,redirect,url_for
from flask_cors import CORS #enable it for all use cases on a domain.
from datetime import datetime 
from dbcon import dbmanager # pymongo db module
from bson.json_util import dumps, loads # convertCursorToJson
from werkzeug.utils import secure_filename # serve_request_data - data add 
import pprint
import os
import ast

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': os.environ['DB_HOST'],
    'db': os.environ['DB']
} # DB 접근설정 : docker-compose.yml 에서 지정해준 환경변수를 가져온다.
CORS(app)

DEBUG = True
KEY = 'request_number' # KEY 값으로 쓸 필드의 이름. 정수형을 기준으로 코드를 작성했다. 


# convertCursorToJson : get_data 에서 쓰이는 함수
# pymongo cursor는 직접적으로 데이터를 출력할 수 없기 때문에
# DBmanager에서 반환된 cursor를 Json 형태로 전환해준다.
def convertCursorToJson(_cursor) :
    lst = list()
    lst.append(_cursor)
    return dumps(lst)
# 현재 날짜와 시간을 문자열 형태로 만들어주는 함수
def getNowTimeStr() :
    return (datetime.now()).strftime("%d/%m/%Y %H:%M:%S")

@app.route('/')
def init_page():
    return 'This is backend'

# @app.route('/back-test')
# def render_test_page():
#     return render_template('test_back_page.html')

"""
Request data
"""
@app.route('/api/request', methods=['POST','GET'])
def serve_request_data():
    dbManager = dbmanager.MongoDbManager(app.config['MONGODB_SETTINGS']['host'],
                                        app.config['MONGODB_SETTINGS']['db'],
                                        'user_requests')
    if request.method == 'POST':
        mode_received = request.form['mode']
        ### ADD data ###
        if mode_received == "add": 
            insert_idx = 0
            last_key_element = dbManager.get_last_element_by(KEY) # 키 필드의 마지막 값을 불러온다.
            if last_key_element == None : # DB가 비어있을 경우 0 부터 시작한다.  
                print("[backend] data empty. start index with 0")
            else : # 마지막 키값에서 1 증가시킨 값을 새로 추가될 데이터의 키값으로 삼는다.
                insert_idx = int(last_key_element[KEY])+1
    
            ipaddr_received = request.remote_addr
            #ipaddr_received = request.form['ip']
            now_time = getNowTimeStr()
            f = request.files['file']
            if (f.filename).endswith('.csv') :
                    print ("[back] user-input file check : it's csv file")
            else : print("[back] user-input file check : not csv file")

            sFilename = secure_filename(f.filename)
            # f.save("./uploads/"+sFilename)
            result = dbManager.add_data({
                            KEY : insert_idx , 
                            'ip': ipaddr_received,
                            'time' : now_time,
                            'file' : sFilename
                            })
            if result != False :
                return jsonify({'result': 'success', 
                                'work': 'add data to DB', 
                                'user_id': insert_idx})
            else :
                return jsonify({'result': 'fail', 
                                'work': 'add data to DB', 
                                })
        ### DELETE data ###
        elif mode_received=="delete" : 
            query = { KEY : int(request.form['key'])}
            result = dbManager.del_data(query)
            if result != False :
                return jsonify({'result': 'success', 
                                'work': 'delete data from DB', 
                                'input':query})
            else : 
                return jsonify({'result': 'fail', 
                                'work': 'delete data from DB', 
                                'input':query})
    ###Get data from DB###
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
    dbManager = dbmanager.MongoDbManager(app.config['MONGODB_SETTINGS']['host'],
                                        app.config['MONGODB_SETTINGS']['db'],
                                        'analyze_result')
    if request.method == 'POST':
        mode_received = request.form['mode']
        ### ADD data ###
        if mode_received == "add": 
            id_received = int(request.form['key'])
            now_time = getNowTimeStr()
            #f = request.files['file']
            result = dbManager.add_data({
                            KEY : id_received , 
                            'time' : now_time,
                            'resultdata': 'dummyResultData'
                            #'file' : f.filename
                            })
            if result != False :
                return jsonify({'result': 'success', 
                                'work': 'add data to DB[analyze_result]', 
                                'user_id': id_received})
            else :
                return jsonify({'result': 'fail', 
                                'work': 'add data to DB[analyze_result]', 
                                'user_id':id_received})
        ### DELETE data ###
        elif mode_received=="delete" : 
            query = { KEY : int(request.form['key'])}
            result = dbManager.del_data(query)
            if result != False :
                return jsonify({'result': 'success', 
                                'work': 'delete data from DB[analyze_result]', 
                                'input':query})
            else : 
                return jsonify({'result': 'fail', 
                                'work': 'delete data from DB[analyze_result]', 
                                'input':query})
    ###Get data from DB###
    elif request.method == 'GET':
        query_received = request.args.get('query')            
        query = ast.literal_eval(query_received)
        data = dbManager.get_data(query)
        return convertCursorToJson(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3050, debug=True)
