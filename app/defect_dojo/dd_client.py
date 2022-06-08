import requests
import json
import string
import random
from datetime import datetime

class DDError(Exception):
    pass
class DefectDojoClient:
    
    ###### INTERNAL CLASS FIELDS #######
    
    base_url_ = ''
    headers_ = {}
    token_ = ''
    username_ = ''
    password_ = ''
    
    
    ###### CLASS PUBLIC METHODS #######
    
    
    def __init__(self, base_url_, username, password):
        self.base_url_ = base_url_
        self.username_ = username
        self.password_ = password
        self.token_ = self.authorize()
    
    def authorize(self):
        self.token_ = self.__authorize()
        if not self.token_:
            print('unable to authorize with defect dojo API')
            return
        self.headers_ = {
            'content-type':'application/json',
            'accept':'application/json',
            'Authorization' : 'Token '+self.token_
        }

    def get_all_findings(self, engagement_ids):
        url = self.base_url_+'/findings/'
        engagements_param = ",".join([str(i) for i in engagement_ids])
        params = {"test__engagement":engagements_param}
        try:
            findings = []
            print('making request to : '+url)
            response = requests.get(url, params=params, headers=self.headers_)
            response_data = json.loads(response.text)            
            next = response_data['next']
            findings = findings + response_data['results']
            
            while next:
                print('making request to : '+next)
                response = requests.get(next, headers=self.headers_)
                response_data = json.loads(response.text)
                findings = findings + response_data['results']
                next = response_data['next']
        except Exception as e:
            print(e)
            return None
        print("Successfully fetched all findings")
        return findings
    
    def get_findings_by_limit(self, engagement_ids, limit, offset):
        url = self.base_url_+'/findings/'
        engagements_param = ",".join([str(i) for i in engagement_ids])
        params = {"test__engagement":engagements_param, "offset": offset, "limit": limit}
        
        try:
            print('making request to : '+url)
            response = requests.get(url, params=params, headers=self.headers_)
            response_data = json.loads(response.text)      
            findings = response_data['results']  
            count = response_data['count']
            next = response_data['next']
            
        except Exception as e:
            print(e)
            return None, None, None
        
        print("Successfully fetched all findings")
        return findings, count, next
    
    def add_product(self, name, description,
                    prod_type, tags = [], prod_numeric_grade = None,
                    business_criticality= None, platform = None, lifecycle = None,
                    origin = None, user_records = None, revenue = None,
                    external_audience = False, internet_accessible = False, enable_simple_risk_acceptance = False,
                    enable_full_risk_acceptance = False , product_manager  = None, technical_contact = None,
                    team_manager = None, regulations = [] ):
        
        url = self.base_url_+'/products/'
        data = {
            "tags": tags,
            "name": name,
            "description": description,
            "prod_numeric_grade": prod_numeric_grade,
            "business_criticality": business_criticality,
            "platform": platform,
            "lifecycle": lifecycle,
            "origin": origin,
            "user_records": user_records,
            "revenue": revenue,
            "external_audience": external_audience,
            "internet_accessible": internet_accessible,
            "enable_simple_risk_acceptance": enable_simple_risk_acceptance,
            "enable_full_risk_acceptance": enable_full_risk_acceptance,
            "product_manager": product_manager,
            "technical_contact": technical_contact,
            "team_manager": team_manager,
            "prod_type": prod_type,
            "regulations": regulations
        }
        try:
            response = requests.post(url, json=data, headers=self.headers_)
            response_data = json.loads(response.text)
        except:
            return None

        return response_data

    def add_engagement(self, target_start, target_end, product_id,
                        tags = [], name = None, description = None, version = None, 
                        first_contacted = None, reason = None, tracker = None, 
                        test_strategy = None, threat_model = False, api_test = False, 
                        pen_test = False, check_list = False, status = None, 
                        engagement_type = None, build_id = None, commit_hash = None,
                        branch_tag = None, source_code_management_uri = None, deduplication_on_engagement = False,
                        lead = None, requester = None,preset = None,
                        report_type = None, build_server= None, source_code_management_server = None,
                        orchestration_engine = None):
        
        url = self.base_url_+'/engagements/'
        
        data = {
                    "tags": tags,
                    "name": name,
                    "description": description,
                    "version": version,
                    "first_contacted": first_contacted,
                    "target_start": target_start,
                    "target_end": target_end,
                    "reason": reason,
                    "tracker": tracker,
                    "test_strategy": test_strategy,
                    "threat_model":threat_model,
                    "api_test": api_test,
                    "pen_test": pen_test,
                    "check_list": check_list,
                    "status": status,
                    "engagement_type": engagement_type,
                    "build_id": build_id,
                    "commit_hash": commit_hash,
                    "branch_tag": branch_tag,
                    "source_code_management_uri": source_code_management_uri,
                    "deduplication_on_engagement": deduplication_on_engagement,
                    "lead": lead,
                    "requester": requester,
                    "preset": preset,
                    "report_type": report_type,
                    "product": product_id,
                    "build_server": build_server,
                    "source_code_management_server": source_code_management_server,
                    "orchestration_engine": orchestration_engine
                }
        try:
            response = requests.post(url, json=data, headers=self.headers_)
            response_data = json.loads(response.text)
        except:
            return None

        return response_data
   
    def create_random_engagment(self):
        
        print("creating random defect dojo product and engagement")
        DD_product_name = ''.join(random.choices(string.ascii_uppercase+string.digits, k=10))
        DD__product_description = ''.join(random.choices(string.ascii_uppercase+string.digits, k=30))
                
        product = self.add_product(DD_product_name, DD__product_description, 1)
        
        if not product:
            raise DDError("Unable to create DefectDojo product")
        
        DD_engagement_name = ''.join(random.choices(string.ascii_uppercase+string.digits, k=10))
        date_now = datetime.today().strftime('%Y-%m-%d')
        
        engagement = self.add_engagement(date_now, date_now,
                                         product['id'], name=DD_engagement_name,
                                         status='In Progress', engagement_type='CI/CD')
        if not engagement:
            raise DDError("Unable to create DefectDojo engagement")
        print("successfully created random defect dojo product and engagement")
        return engagement['id']
    
    
    ###### CLASS PRIVATE METHODS #######
    
    def __authorize(self):
        url = self.base_url_+'/api-token-auth/'
        print("getting DefectDojo API key")
        headers = {
            'content-type':'application/json',
            'accept':'application/json'
        }
        data = {
            'username': self.username_,
            'password': self.password_
        }
        try:
            response = requests.post(url, json=data, headers=headers)
            response_data = json.loads(response.text)
        except:
            return None
        
        return response_data['token']      

