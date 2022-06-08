import os

# Defect Dojo configuration

DD_BASE_URL = os.getenv('DEFECT_DOJO_BASE_URL')
DD_USERNAME = os.getenv('DEFECT_DOJO_USERNAME')
DD_PASSWORD = os.getenv('DEFECT_DOJO_PASSWORD')

# Jenkins Configuration

JENKINS_BASE_URL = os.getenv('JENKINS_BASE_URL')
JENKINS_USERNAME = os.getenv('JENKINS_USERNAME')
JENKINS_PASSWORD = os.getenv('JENKINS_PASSWORD')

# User API Configuration
USER_API_BASE_URL = os.getenv('USER_API_BASE_URL')
USER_NOTF_API_BASE_URL = os.getenv('USER_NOTF_API_BASE_URL')
SSO_API_BASE_URL = os.getenv('SSO_API_BASE_URL')

# SERVER configuration

SERVER_IP = '0.0.0.0'
SERVER_PORT = 5000
