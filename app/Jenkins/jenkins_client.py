import jenkins
import os
from database import database
from aws import s3
from Jenkins import config, config_xml_file_manager

class JenkinsError(Exception):
    pass

class JenkinsClient:
    
    client_ = None
    local_config_xml_folder_ = None
    s3_config_xml_folder_ = None
    
    def __init__(self, base_url, username, password):
        try:
            self.client_ = jenkins.Jenkins(base_url,
                            username = username,
                            password = password)
            self.local_config_xml_folder_ = config.LOCAL_CONFIG_XML_FOLDER
            self.s3_config_xml_folder_ = config.S3_CONFIG_XML_FOLDER 
        except Exception as e:
            raise JenkinsError("unable to connect to jenkins")

    def create_job(self,  name, engagment_id, scan_profile_id):
        config_xml = self.__get_config_xml_for_scan(engagment_id, scan_profile_id)
        try:
            print("creating a jenkins job for the scan")
            self.client_.create_job(name, config_xml)
        except Exception as e:
            print(e)
            raise JenkinsError("Unable to create jenkins job")    
        print('job created successfully with name - '+name)
                
    
    def __get_config_xml_for_scan(self, engagment_id, scan_profile_id):
        config_xml = None
        
        result_set = database.get_scan_profile(scan_profile_id)
        row = result_set[0]
        config_xml_file_name =  row[5]
    
        local_config_xml_file_path = self.local_config_xml_folder_+config_xml_file_name
        s3_config_xml_file_path = self.s3_config_xml_folder_+config_xml_file_name
        
        if not os.path.exists(local_config_xml_file_path):
            print('config_xml file doesn''t exist at local, downloading from s3 ('+s3_config_xml_file_path+')')
            s3.download_file( config.S3_BUCKET_NAME , s3_config_xml_file_path, local_config_xml_file_path)
            print('downloaded file '+local_config_xml_file_path)
        
        engagment_id_parameter = [{
                                    'name':'engagment_id',
                                    'value': engagment_id
                                    }]
        config_xml_file_manager.insertStringParameters(local_config_xml_file_path, engagment_id_parameter)
        
        with open(local_config_xml_file_path, 'r') as file:
                config_xml = file.read()
        
        file.close()
        
        print('deleting file '+local_config_xml_file_path)
        os.remove(local_config_xml_file_path)
        
        return config_xml