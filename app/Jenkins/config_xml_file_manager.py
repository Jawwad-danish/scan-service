from aws import s3
from database import database
from xml.etree import ElementTree
from Jenkins import config
import os

def create_scan_profile_xml_config(scan_profile_id, scan_type_id, scan_profile_parameters):
    
    #getting all scan_type template file name
    result_set = database.get_scan_type(str(scan_type_id))
    row = result_set[0]
    s3_template_file_path = row[3]
    scan_type_name = row[1]
    
    file_name = scan_type_name+scan_profile_id+'.xml'
    
    local_file_path = config.LOCAL_CONFIG_XML_FOLDER+file_name
        
    s3.download_file(config.S3_BUCKET_NAME, s3_template_file_path, local_file_path)
    
    insertStringParameters(local_file_path, scan_profile_parameters)
    
    s3_profile_file_path = config.S3_CONFIG_XML_FOLDER+file_name
    
    s3.upload_file(config.S3_BUCKET_NAME, local_file_path, s3_profile_file_path)
    
    if os.path.exists(local_file_path):
        os.remove(local_file_path)
    
    return file_name


def insertStringParameters(xmlfile, parameters=[]):
  
    tree = ElementTree.parse(xmlfile)
    root = tree.getroot()

    parameterDefinitions = root.find("properties").find("hudson.model.ParametersDefinitionProperty").find("parameterDefinitions")
    
    for param in parameters:
        head = ElementTree.SubElement(parameterDefinitions, "hudson.model.StringParameterDefinition")
        for key in param:
            if key == 'name':
                node = ElementTree.SubElement(head, 'name')
                node.text = param[key]
            if key == 'value':
                node = ElementTree.SubElement(head, 'defaultValue')
                node.text = param[key]
            
        node = ElementTree.SubElement(head, "trim")
        node.text = "false"    
            
    tree.write(xmlfile)

