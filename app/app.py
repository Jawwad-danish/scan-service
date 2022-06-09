# main app file flask server
# created by MUHAMMAD JAWWAD DANISH


from flask import Flask, jsonify, make_response, redirect, request
import config
from database import database
from constants import constants
import json
import requests
from functools import wraps
from datetime import datetime
from defect_dojo.dd_client import DefectDojoClient , DDError
from Jenkins import config_xml_file_manager
from Jenkins.jenkins_client import JenkinsClient, JenkinsError
import jwt

app = Flask(__name__)

def makeFormattedResponse( message, status_code, data = None):
    body = {"message":message, "status_code":status_code}
    if data:
        body['data'] = data
    response = make_response(jsonify(body))
    response.status_code = status_code
    return response

def validate_token(func):
    @wraps(func)
    def inner1(*args, **kwargs):
        try:
            is_valid = False
            url = config.USER_API_BASE_URL+'/user/validatetoken'
            #calling usersvc to validate token
            token_header = request.headers['authorization']
            auth_token = token_header.split(maxsplit=1)[1]
            payload = {'jwt' : auth_token} 
            
            response = requests.post(url, json=payload)
            response = json.loads(response.text)
            is_valid = response['data']
            if is_valid:
                return func(*args, **kwargs)
            else:
                return makeFormattedResponse("authentication token is invalid",500)
        except Exception as e:
            return makeFormattedResponse(str(e), 500)
                 
    return inner1

@app.route("/health_check", methods = ['GET'])
def health_check():
    return makeFormattedResponse("I AM Alive",200,{
        "datetime": datetime.today().strftime('%Y-%m-%d:%H:%M:%S')
    })

@app.route("/product/<id>/finding", methods = ['GET'])
@validate_token
def get_product_findings(id):
    data = []
    try:
        result_set = database.get_all_scan_by_product(id)
        next_url = None
        engagement_ids = []
        for row in result_set:
            engagement_ids.append(row[2])
        
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        
        if not limit:
            limit = 25
        if not offset:
            offset = 0
        
        ddClient = DefectDojoClient( config.DD_BASE_URL, config.DD_USERNAME, config.DD_PASSWORD)
        findings, total_count, next = ddClient.get_findings_by_limit(engagement_ids, limit, offset)
        print(request.url.split("?")[0])
        if next:
            next_url = request.url.split("?")[0]+"?limit="+str(limit)+"&offset="+str(int(offset)+int(limit))
        
        data = {"total_count":total_count, "fetch_count":len(findings), "next_url":next_url, "findings":findings}
                   
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    
    
    return makeFormattedResponse("Successfully fetched findings for product id :"+id ,200 ,data)

@app.route("/component/<id>/finding", methods = ['GET'])
@validate_token
def get_component_findings(id):
    data = []
    try:
        result_set = database.get_all_scan_by_component(id)
        next_url = None
        engagement_ids = []
        for row in result_set:
            engagement_ids.append(row[2])
        
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        
        if not limit:
            limit = 25
        if not offset:
            offset = 0
        
        ddClient = DefectDojoClient( config.DD_BASE_URL, config.DD_USERNAME, config.DD_PASSWORD)
        findings, total_count, next = ddClient.get_findings_by_limit(engagement_ids, limit, offset)
        print(request.url.split("?")[0])
        if next:
            next_url = request.url.split("?")[0]+"?limit="+str(limit)+"&offset="+str(int(offset)+int(limit))
        
        data = {"total_count":total_count, "fetch_count":len(findings), "next_url":next_url, "findings":findings}
                   
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    
    
    return makeFormattedResponse("Successfully fetched findings for component id :"+id ,200 ,data)

@app.route("/scan/<id>/finding", methods = ['GET'])
@validate_token
def get_scan_finding(id):
    data = []
    try:
        result_set = database.get_scan(id)
        next_url = None
        engagement_ids = []
        for row in result_set:
            engagement_ids.append(row[2])
        
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        
        if not limit:
            limit = 25
        if not offset:
            offset = 0
        
        ddClient = DefectDojoClient( config.DD_BASE_URL, config.DD_USERNAME, config.DD_PASSWORD)
        findings, total_count, next = ddClient.get_findings_by_limit(engagement_ids, limit, offset)
        print(request.url.split("?")[0])
        if next:
            next_url = request.url.split("?")[0]+"?limit="+str(limit)+"&offset="+str(int(offset)+int(limit))
        
        data = {"total_count":total_count, "fetch_count":len(findings), "next_url":next_url, "findings":findings}
                   
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)

    return makeFormattedResponse("Successfully fetched findings for component id :"+id ,200 ,data)
    
@app.route("/scan", methods = ['POST'])
@validate_token
def setup_scan():
    payload = request.json  
    
    try:
        #getting user id from JWT
        token_header = request.headers['authorization']
        auth_token = token_header.split(maxsplit=1)[1]
        token_payload = jwt.decode(auth_token, options={"verify_signature": False})
        user_id = token_payload['userid']
        
        # creating a product and engagment in defectdojo
        ddClient = DefectDojoClient( config.DD_BASE_URL, config.DD_USERNAME, config.DD_PASSWORD)
        engagment_id = ddClient.create_random_engagment()
        
        print("created an engagement at DefectDojo")
        
        # inserting a scan record with jenkins_job_name = not_set,
        # just to get a scan_id        
        scan_profile_id = payload['scan_profile_id']
        name = payload['name']
        description = payload['description']
        schedule = payload['schedule']
        setup_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = constants.SCAN_STATUS_IN_PROGRESS
        
        scan_id = database.add_scan(scan_profile_id=scan_profile_id, engagment_id=engagment_id,
                                         user_id=user_id, jenkins_job_id='NOT-SET', name=name, description=description,
                                         schedule=schedule, setup_date=setup_date, status=status)
        print("created a record for scan in database")
        
        # creating a jenkins job
        jenkinsClient = JenkinsClient(config.JENKINS_BASE_URL, config.JENKINS_USERNAME, config.JENKINS_PASSWORD)
        print("created jenkins client")
        jenkins_job_name = 'alpha-scale-scan-'+str(scan_id)
        jenkinsClient.create_job(jenkins_job_name,str(engagment_id),str(scan_profile_id))
        print("created jenkins job")
        
        # updating scan with jenkins job name
        database.update_scan(scan_id=scan_id, scan_profile_id=scan_profile_id, engagment_id=engagment_id,   
                                         user_id=user_id, jenkins_job_id=jenkins_job_name, name=name, description=description,
                                         schedule=schedule, setup_date=setup_date, status=status)
        print("updated scan record with jenkins job name in database")
        
        data = {"id":scan_id}
    
    except DDError as e:
        return makeFormattedResponse(str(e),500)
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    except JenkinsError as e:
        database.delete_scan(scan_id)
        return makeFormattedResponse(str(e), 500)
    except Exception as e:
        return makeFormattedResponse(str(e),500)
    
    return makeFormattedResponse("scan added successfully", 200, data)
        
@app.route("/scan/<id>", methods = ['GET'])
@validate_token
def get_scan(id):
    pass

@app.route("/scan/<id>", methods = ['UPDATE'])
@validate_token
def update_scan(id):
    pass

@app.route("/scan/<id>", methods = ['DELETE'])
@validate_token
def delete_scan(id):
    pass


####### SCAN_TYPE

@app.route("/scan_type", methods = ['GET'])
@validate_token
def get_all_scan_types():
   
    data = []
    try:
        result_set = database.get_all_scan_types()        # getting scan type records
        for row in result_set:
            data.append({
                'id':row[0],
                'name':row[1],
                'description':row[2],
                'jenkins_template_cfg_obj_name':row[3]
            })
    
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    
    
    return makeFormattedResponse("Successfully fetched scan types" ,200 ,data)

@app.route("/scan_type/<id>", methods = ['GET'])
@validate_token
def get_scan_type(id):
    data = {}
    try:
        # getting scan type record
        result_set = database.get_scan_type(id)        
        for row in result_set:
            data = {
                'id':row[0],
                'name':row[1],
                'description':row[2],
                'jenkins_template_cfg_obj_name':row[3]
            }
    
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    
    
    return makeFormattedResponse("Successfully fetched scan types" ,200 ,data)

@app.route("/scan_type", methods = ['POST'])
@validate_token
def add_scan_type():
    payload = request.json  
    try:
        if 'parameters' in payload:
            scan_type_id = database.add_scan_type(payload['name'], payload['description'], payload['jenkins_cfg_obj_name'], payload['parameters'])
        else:
            scan_type_id = database.add_scan_type(payload['name'], payload['description'], payload['jenkins_cfg_obj_name'])
        data = {"id":scan_type_id}
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    except:
        return makeFormattedResponse("internal server error",500)
    
    return makeFormattedResponse("scan_type added successfully", 200, data)

@app.route("/scan_type/<id>", methods = ['PUT'])
@validate_token
def update_scan_type(id):
    payload = request.json  
    try:
        if 'parameters' in payload:
            database.update_scan_type(id, payload['name'], payload['description'], payload['jenkins_cfg_obj_name'], payload['parameters'])
        else:
            database.update_scan_type(id, payload['name'], payload['description'], payload['jenkins_cfg_obj_name'])
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    return makeFormattedResponse("scan_type updated successfully", 200)

@app.route("/scan_type/<id>", methods = ['DELETE'])
@validate_token
def delete_scan_type(id):
    try:
        database.delete_scan_type(id)
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)

    return makeFormattedResponse("successfully deleted scan_type of id = "+id ,200)

@app.route("/scan_type/<id>/parameters", methods = ['GET'])
@validate_token
def get_all_scan_type_prameters(id):
    data = []
    try:
        # getting scan type record
        result_set = database.get_all_scan_type_parameters_of_scan_type(id)        
        for row in result_set:
            data.append( {
                'id':row[0],
                'name':row[1],
                'description':row[2],
            })
    
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    
    
    return makeFormattedResponse("Successfully fetched scan type parameters" ,200 ,data)

@app.route("/scan_type/<id>/parameters", methods = ['POST'])
@validate_token
def add_scan_type_prameters(id):
    payload = request.json  
    try:
        database.add_scan_type_parameters(id, payload['parameters'])
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    except:
        return makeFormattedResponse("internal server error",500)
    
    return makeFormattedResponse("scan_type parameters added successfully", 200)

@app.route("/scan_type/parameters/<id>", methods = ['PUT'])
@validate_token
def update_scan_type_prameter(id):
    payload = request.json  
    try:
        database.update_scan_type_parameter(id, payload['name'], payload['description'])
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    except:
        return makeFormattedResponse("internal server error",500)
    
    return makeFormattedResponse("scan_type parameters added successfully", 200)
    
@app.route("/scan_type/parameters/<id>", methods = ['DELETE'])
@validate_token
def delete_scan_type_prameter(id):
    try:
        database.delete_scan_type_parameter(id)
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    except:
        return makeFormattedResponse("internal server error",500)
    
    return makeFormattedResponse("scan_type parameter deleted successfully", 200)

###### SCAN_PROFILE

@app.route("/scan_profile", methods = ['POST'])
def add_scan_profile():
    payload = request.json  
    try:        
        if 'parameters' in payload:
            scan_profile_id = database.add_scan_profile(payload['name'], payload['description'], 
                                      payload['scan_type_id'], payload['component_id'],
                                      payload['parameters'])
        else:
            scan_profile_id = database.add_scan_profile(payload['name'], payload['description'],
                                      payload['scan_type_id'], payload['component_id'])
        
        jenkins_cfg_file_name = config_xml_file_manager.create_scan_profile_xml_config(str(scan_profile_id), payload['scan_type_id'], payload['parameters'])
        
        database.update_scan_profile(scan_profile_id, payload['name'], payload['description'],
                                      payload['scan_type_id'], payload['component_id'], jenkins_cfg_file_name)
        
        data = {"id":scan_profile_id}
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    return makeFormattedResponse("scan_profile added successfully", 200, data)
    
@app.route("/scan_profile/<id>", methods = ['GET'])
@validate_token
def get_scan_profile(id):
    
    data = None
    try:
        result_set = database.get_scan_profile(id)
        
        # getting scan profile record
        row = result_set[0]
        data = {
            'id':row[0],
            'name':row[1],
            'description':row[2],
            'scan_type_id':row[3],
            'component_id':row[4],
            'jenkins_cfg_obj_name':row[5]
        }
        parameters = []
        
        #getting parameters for fetched scan profile
        result_set = database.get_all_scan_profile_parameters_of_scan_profile(id)
    
        for row in result_set:
            parameters.append({row[0]:row[1]})

        data['parameters'] = parameters
    
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    
    
    return makeFormattedResponse("Successfully fetched scan profile of id = "+id ,200 ,data)

@app.route("/scan_profile/<id>", methods = ['PUT'])
@validate_token
def update_scan_profile(id):
    payload = request.json  
    try:
        if 'parameters' in payload:
            database.update_scan_profile(id, payload['name'], payload['description'],
                                         payload['scan_type_id'],payload['component_id'],
                                         payload['parameters'])
        else:
            database.update_scan_profile(id, payload['name'], payload['description'],
                                         payload['scan_type_id'],payload['component_id'])
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    return makeFormattedResponse("scan_profile updated successfully", 200)

@app.route("/scan_profile/<id>", methods = ['DELETE'])
@validate_token
def delete_scan_profile(id):
    try:
        database.delete_scan_profile(id)
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)

    return makeFormattedResponse("successfully deleted scan_profile of id = "+id ,200)

###### PRODUCT

@app.route("/product", methods = ['GET'])
@validate_token
def get_all_products():
    data = []
    try:
        result_set = database.get_all_products()        # getting scan type records
        for row in result_set:
            data.append({
                'id':row[0],
                'name':row[1],
                'description':row[2],
            })
    
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    
    
    return makeFormattedResponse("Successfully fetched products" ,200 ,data)

@app.route("/product/<id>", methods = ['GET'])
@validate_token
def get_product(id):
    data = {}
    try:
        # getting scan type record
        result_set = database.get_product(id)        
        for row in result_set:
            data = {
                'id':row[0],
                'name':row[1],
                'description':row[2],
            }
    
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    
    
    return makeFormattedResponse("Successfully fetched product" ,200 ,data)

@app.route("/product", methods = ['POST'])
@validate_token
def add_product():
    payload = request.json  
    try:
        token_header = request.headers['authorization']
        auth_token = token_header.split(maxsplit=1)[1]
        token_payload = jwt.decode(auth_token, options={"verify_signature": False})
        
        user_id = token_payload['userid']
        scan_type_id = database.add_product(payload['name'], payload['description'], user_id)
        
        data = {"id":scan_type_id}
    
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    except:
       return makeFormattedResponse("internal server error",500)
    
    return makeFormattedResponse("product added successfully", 200, data)

@app.route("/product/<id>", methods = ['PUT'])
@validate_token
def update_product(id):
    payload = request.json  
    try:
        database.update_product(id, payload['name'], payload['description'])
        
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    return makeFormattedResponse("product updated successfully", 200)

@app.route("/product/<id>", methods = ['DELETE'])
@validate_token
def delete_product(id):
    try:
        database.delete_product(id)
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)

    return makeFormattedResponse("successfully deleted product of id = "+id ,200)

###### COMPONENT

@app.route("/component", methods = ['GET'])
@validate_token
def get_all_components():
    data = []
    try:
        result_set = database.get_all_components()        # getting scan type records
        for row in result_set:
            data.append({
                'id':row[0],
                'name':row[1],
                'description':row[2],
                'product_id':row[3]
            })
    
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    
    
    return makeFormattedResponse("Successfully fetched components" ,200 ,data)

@app.route("/component/<id>", methods = ['GET'])
@validate_token
def get_component(id):
    data = {}
    try:
        # getting scan type record
        result_set = database.get_component(id)        
        for row in result_set:
            data = {
                'id':row[0],
                'name':row[1],
                'description':row[2],
                'product_id':row[3]
            }
    
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    
    
    return makeFormattedResponse("Successfully fetched component" ,200 ,data)

@app.route("/component", methods = ['POST'])
@validate_token
def add_component():
    payload = request.json  
    try:
        scan_type_id = database.add_component(payload['name'], payload['description'], payload['product_id'])
        data = {"id":scan_type_id}
    
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    except:
        return makeFormattedResponse("internal server error",500)
    
    return makeFormattedResponse("component added successfully", 200, data)

@app.route("/component/<id>", methods = ['PUT'])
@validate_token
def update_component(id):
    payload = request.json  
    try:
        database.update_component(id, payload['name'], payload['description'], payload['product_id'])
        
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)
    return makeFormattedResponse("component updated successfully", 200)

@app.route("/component/<id>", methods = ['DELETE'])
@validate_token
def delete_component(id):
    try:
        database.delete_component(id)
    except database.MariadbError as e:
        return makeFormattedResponse(str(e),500)
    except database.ConnectionError as e:
        return makeFormattedResponse(str(e),500)
    except database.OperationError as e:
        return makeFormattedResponse(str(e),404)

    return makeFormattedResponse("successfully deleted component of id = "+id ,200)



# starting flask server.
if __name__ == '__main__':
    app.run( config.SERVER_IP, port=config.SERVER_PORT,debug = True)