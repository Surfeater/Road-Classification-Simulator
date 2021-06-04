from flask import Flask, jsonify, request, render_template
from flask_restplus import Api,Resource, fields

from datetime import datetime 
from bson.json_util import dumps, loads # convertCursorToJson
from werkzeug.utils import secure_filename # serve_request_data - data add 
import pprint
import os
import ast

from dbcon import dbmanager # pymongo db module


DEBUG = True
app = Flask(__name__)
api = Api(app, version='3.0', title='Surface-Detect-Simulator API', 
        description='API for user_request data')

ns_rq = api.namespace('requests', description = 'analysis request data operations')
ns_rs = api.namespace('results', description = 'analysis result data operations')

app.config['MONGODB_SETTINGS'] = { 'host': os.environ['DB_HOST'],
                                    'db': os.environ['DB']} 
DAO = dbmanager.MongoDbManager( app.config['MONGODB_SETTINGS']['host'], 
                                app.config['MONGODB_SETTINGS']['db'],'user_requests')
KEY = 'request_number'  

analysis_request = api.model('Analysis request',{
    #'_id' : fields.Wildcard(readonly=True,description="identifier mongoDB automatically generate"),
    'request_number' : fields.Integer(readonly=True, description="the request unique identifier"),
    'ip' : fields.String(readonly=True, description="ip of analysis requested"),
    'time' : fields.String(readonly=True,description="time of analysis requested"),
    'filepath' : fields.String(required=True, description= "filepath of input for analysis")
})

def getNowTimeStr() :
    return (datetime.now()).strftime("%d/%m/%Y %H:%M:%S")


@ns_rq.route('/')
class AnalysisRequestList (Resource) :
    """Show a list of all analysis requests"""
    @ns_rq.doc('list_analysis_requests')
    @ns_rq.marshal_list_with(analysis_request)
    def get (self) :
        '''List all requests'''
        result = list()
        for x in DAO.get_data({}) :
            result.append(x)
        return result
    
    @ns_rq.doc('list_analysis_requests')
    @ns_rq.expect(analysis_request)
    @ns_rq.marshal_list_with(analysis_request, code=201)
    def post(self):
        '''create new request'''
        received_data = api.payload
        ipaddr_received =  request.remote_addr #received_data['ip'] #ipaddr_received = request.form['ip']
        now_time = getNowTimeStr() #received_data['time']     
        filepath = received_data['filepath'] #f = request.files['file']
        # sFilename = secure_filename(f.filename)
        # f.save("./uploads/"+sFilename)

        # if (f.filename).endswith('.csv') :
        #         print ("[back] user-input file check : it's csv file")
        # else : print("[back] user-input file check : not csv file")

        generated_req_num = 0
        last_key_element = DAO.get_last_element_by(KEY) # 키 필드의 마지막 값을 불러온다.
        if last_key_element == None : # DB가 비어있을 경우 0 부터 시작한다.  
            print("[backend] data empty. start request_number with 0")
        else : # 마지막 키값에서 1 증가시킨 값을 새로 추가될 데이터의 키값으로 삼는다.
            generated_req_num = int(last_key_element[KEY])+1
        
        formed_data = {  KEY : generated_req_num , 
                        'ip': ipaddr_received,
                        'time' : now_time,
                        'filepath' : filepath }
        
        DAO.add_data(formed_data)
        result = DAO.get_data({KEY : generated_req_num})
        return loads(dumps(result)), 201


@ns_rq.route('/<int:request_number>')
@ns_rq.response(404, 'Analyze request not found')
@ns_rq.param('request_number', 'The task identifier')
class AnalysisRequest(Resource):
    '''Show a single analysis_request item and lets you delete them'''
    @ns_rq.doc('get_analyze_request')
    @ns_rq.marshal_with(analysis_request)
    def get(self, request_number):
        '''Get a request by request_number'''
        query = {KEY : request_number}
        result = DAO.get_data(query)
        return loads(dumps(result))

    @ns_rq.doc('delete_analyze_request')
    @ns_rq.response(204, 'analysis_request deleted')
    def delete(self, request_number):
        '''Delete a request by request_number'''
        query = {KEY : request_number}
        DAO.del_data(query)
        return '', 204

# """
# Request data
# """
# @app.route('/api/request', methods=['POST','GET'])
# def analysisRequestList():
#     # dbManager = dbmanager.MongoDbManager(app.config['MONGODB_SETTINGS']['host'],
#     #                                     app.config['MONGODB_SETTINGS']['db'],
#     #                                     'user_requests')
#     if request.method == 'POST':
#         generated_req_num = 0
#         last_key_element = dbManager.get_last_element_by(KEY) # 키 필드의 마지막 값을 불러온다.
#         if last_key_element == None : # DB가 비어있을 경우 0 부터 시작한다.  
#             print("[backend] data empty. start index with 0")
#         else : # 마지막 키값에서 1 증가시킨 값을 새로 추가될 데이터의 키값으로 삼는다.
#             generated_req_num = int(last_key_element[KEY])+1

#         ipaddr_received = request.remote_addr
#         #ipaddr_received = request.form['ip']
#         now_time = getNowTimeStr()
#         f = request.files['file']
#         if (f.filename).endswith('.csv') :
#                 print ("[back] user-input file check : it's csv file")
#         else : print("[back] user-input file check : not csv file")

#         sFilename = secure_filename(f.filename)
#         # f.save("./uploads/"+sFilename)
#         result = dbManager.add_data({
#                         KEY : generated_req_num , 
#                         'ip': ipaddr_received,
#                         'time' : now_time,
#                         'file' : sFilename
#                         })
#         if result != False :
#             return jsonify({'result': 'success', 
#                             'work': 'add data to DB', 
#                             'user_id': generated_req_num})
#         else :
#             return jsonify({'result': 'fail', 
#                             'work': 'add data to DB', 
#                             })
#     ###Get data from DB###
#     elif request.method == 'GET':
#         # query_received = request.args.get('query')            
#         # query = ast.literal_eval(query_received)
#         result = dbManager.get_data({})
#         return convertCursorToJson(result)

# @app.route('/api/request/<int:request_number>') #methods=['GET','DELETE'])
# def analysisRequest(Resource):
#     # dbManager = dbmanager.MongoDbManager(app.config['MONGODB_SETTINGS']['host'],
#     #                                     app.config['MONGODB_SETTINGS']['db'],
#     #                                     'user_requests')
#     request_number_received = request_number #int(request.args.get('request_number'))
#     query = { KEY : request_number_received}

#     if request.method == 'GET':
#         result = dbManager.get_data(query)
#         return convertCursorToJson(result)

#     elif request.method == 'DELETE' :    
#         result = dbManager.del_data(query)
#         if result != False :
#             return jsonify({'result': 'success', 
#                             'work': 'delete data from DB', 
#                             'input':query})
#         else : 
#             return jsonify({'result': 'fail', 
#                             'work': 'delete data from DB', 
#                             'input':query})

# """
# Result data
# """
# @app.route('/api/result', methods=['POST','GET'])
# def serve_result_data():
#     # dbManager = dbmanager.MongoDbManager(app.config['MONGODB_SETTINGS']['host'],
#     #                                     app.config['MONGODB_SETTINGS']['db'],
#     #                                     'analyze_result')
#     if request.method == 'POST':
#         mode_received = request.form['mode']
#         ### ADD data ###
#         if mode_received == "add": 
#             id_received = int(request.form[KEY])
#             now_time = getNowTimeStr()
#             #f = request.files['file']
#             result = dbManager.add_data({
#                             KEY : id_received , 
#                             'time' : now_time,
#                             'resultdata': 'dummyResultData'
#                             #'file' : f.filename
#                             })
#             if result != False :
#                 return jsonify({'result': 'success', 
#                                 'work': 'add data to DB[analyze_result]', 
#                                 'user_id': id_received})
#             else :
#                 return jsonify({'result': 'fail', 
#                                 'work': 'add data to DB[analyze_result]', 
#                                 'user_id':id_received})
#         ### DELETE data ###
#         elif mode_received=="delete" : 
#             query = { KEY : int(request.form[KEY])}
#             result = dbManager.del_data(query)
#             if result != False :
#                 return jsonify({'result': 'success', 
#                                 'work': 'delete data from DB[analyze_result]', 
#                                 'input':query})
#             else : 
#                 return jsonify({'result': 'fail', 
#                                 'work': 'delete data from DB[analyze_result]', 
#                                 'input':query})
#     ###Get data from DB###
#     elif request.method == 'GET':
#         query_received = request.args.get('query')            
#         query = ast.literal_eval(query_received)
#         data = dbManager.get_data(query)
#         return convertCursorToJson(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3050, debug=True)
