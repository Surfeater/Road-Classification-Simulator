from flask import Flask, jsonify, request, render_template
from flask_restplus import Api,Resource, fields

from datetime import datetime 
from bson.json_util import dumps, loads # convertCursorToJson
from werkzeug.utils import secure_filename # serve_request_data - data add 
from flask_cors import CORS
import pprint
import os
import ast

from dbcon import dbmanager # pymongo db module


DEBUG = True
app = Flask(__name__)
CORS(app)
api = Api(app, version='3.0', title='Road Classification Simulator API', 
        description='API for analysis request & analysis result')

ns_rq = api.namespace('requests', description = 'analysis request data operations')
ns_rs = api.namespace('results', description = 'analysis result data operations')

app.config['MONGODB_SETTINGS'] = { 'host': os.environ['DB_HOST'],
                                    'db': os.environ['DB']} 
collections = ['analysis_request','analysis_result']
DAO = dbmanager.MongoDbManager( app.config['MONGODB_SETTINGS']['host'], 
                                app.config['MONGODB_SETTINGS']['db'], collections[0])
KEY = 'request_number'  

analysis_request = ns_rq.model('Analysis request',{
    #'_id' : fields.Wildcard(readonly=True,description="identifier mongoDB automatically generate"),
    'request_number' : fields.Integer(readonly=True, description="the request unique identifier (auto generated)"),
    'ip' : fields.String(readonly=True, description="ip of analysis requested (auto generated)"),
    'time' : fields.String(readonly=True,description="time of analysis requested (auto generated)"),
    'filepath' : fields.String(required=True, description= "filepath of input for analysis")
})

analysis_result = ns_rs.model('Analysis result',{
    'request_number' : fields.Integer(required=True, description="the request unique identifier"),
    'time' : fields.String(readonly=True,description="time of analysis finished"),
    'input_filepath' : fields.String(required=True, description= "filepath of input data stored in file system"),
    'result_filepath' : fields.String(required=True, description= "filepath of result data stored in file system")
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
        DAO.set_cursor(collections[0])
        result = list()
        for x in DAO.get_data({}) :
            result.append(x)
        return result
    
    @ns_rq.doc('create_analysis_request')
    @ns_rq.expect(analysis_request)
    @ns_rq.marshal_list_with(analysis_request, code=201)
    def post(self):
        '''create new request'''
        DAO.set_cursor(collections[0])
        received_data = api.payload
        ipaddr_received =  request.remote_addr 
        now_time = getNowTimeStr()      
        filepath = received_data['filepath'] 

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
@ns_rq.response(404, 'Analysis request not found')
@ns_rq.param('request_number', 'The request identifier')
class AnalysisRequest(Resource):
    '''Show a single analysis_request item and lets you delete them'''
    @ns_rq.doc('get_analyze_request')
    @ns_rq.marshal_with(analysis_request)
    def get(self, request_number):
        '''Get a request by request_number'''
        DAO.set_cursor(collections[0])
        query = {KEY : request_number}
        result = DAO.get_data(query)
        return loads(dumps(result))

    @ns_rq.doc('delete_analyze_request')
    @ns_rq.response(204, 'analysis_request deleted')
    def delete(self, request_number):
        '''Delete a request by request_number'''
        DAO.set_cursor(collections[0])
        query = {KEY : request_number}
        DAO.del_data(query)
        return '', 204

#########################################################################
@ns_rs.route('/')
class AnalysisResultList (Resource) :
    """Show a list of all analysis results"""
    @ns_rs.doc('list_analysis_results')
    @ns_rs.marshal_list_with(analysis_result)
    def get (self) :
        '''List all results'''
        DAO.set_cursor(collections[1])
        result = list()
        for x in DAO.get_data({}) :
            result.append(x)
        return result
    
    @ns_rs.doc('create_analysis_result')
    @ns_rs.response(403, 'NOT allowed create result_data for not existing request_number')
    @ns_rs.expect(analysis_result)
    @ns_rs.marshal_list_with(analysis_result, code=201)
    def post(self):
        '''create new result data (caution : request number must exist in analysis request)'''
        received_data = api.payload
        received_request_number = received_data['request_number']
        now_time = getNowTimeStr() #received_data['time']
        input_filepath = received_data['input_filepath'] 
        result_filepath = received_data['result_filepath']
        
        DAO.set_cursor(collections[0])
        if DAO.count_data_by({KEY : received_request_number}) == 0 :
            return '', 403

        formed_data =  {
                        'request_number' : received_request_number,
                        'time' : now_time,
                        'input_filepath' : input_filepath,
                        'result_filepath' : result_filepath
                    }
        
        DAO.set_cursor(collections[1])
        DAO.add_data(formed_data)
        result = DAO.get_data({KEY : received_request_number})
        return loads(dumps(result)), 201


@ns_rs.route('/<int:request_number>')
@ns_rs.response(404, 'Analysis result not found')
@ns_rs.param('request_number', 'The result identifier')
class AnalysisResult(Resource):
    '''Show a single analysis_result item and lets you delete them'''
    @ns_rs.doc('get_analyze_request')
    @ns_rs.marshal_with(analysis_result)
    def get(self, request_number):
        '''Get a analysis_result by request_number'''
        DAO.set_cursor(collections[1])
        query = {KEY : request_number}
        result = DAO.get_data(query)
        return loads(dumps(result))

    @ns_rs.doc('delete_analysis_request')
    @ns_rs.response(204, 'analysis_result deleted')
    def delete(self, request_number):
        '''Delete a analysis_result by request_number'''
        DAO.set_cursor(collections[1])
        query = {KEY : request_number}
        DAO.del_data(query)
        return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3050, debug=True)
