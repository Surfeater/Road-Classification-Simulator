
from flask import Flask, jsonify, request, render_template,make_response,session,redirect,url_for
from flask_cors import CORS
from datetime import datetime
from dbcon import dbmanager
from bson.json_util import dumps, loads
import pprint
import os
import ast

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'host': os.environ['DB_HOST'],
    'db': os.environ['DB']
}

print(app.config['MONGODB_SETTINGS']['host'])
print(type(app.config['MONGODB_SETTINGS']['host']))
print(app.config['MONGODB_SETTINGS']['db'])
print(type(app.config['MONGODB_SETTINGS']['db']))

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

@app.route('/')
def init_page():
    return redirect(url_for('render_test_page'))

@app.route('/back-test')
def render_test_page():
    return render_template('test_back_page.html')

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
            id_received = request.form['key']
            ipaddr_received = request.remote_addr
            #ipaddr_received = request.form['ip']
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
    dbManager = dbmanager.MongoDbManager(app.config['MONGODB_SETTINGS']['host'],
                                        app.config['MONGODB_SETTINGS']['db'],
                                        'analyze_result')
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
                            'resultdata': 'dummyResultData'
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3050, debug=True)
