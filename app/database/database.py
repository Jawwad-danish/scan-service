import mariadb
from database import config

class ConnectionError(Exception):
    pass
class MariadbError(Exception):
    pass
class OperationError(Exception):
    pass
 
def get_connection():
    try:
        conn = mariadb.connect(
            user = config.DB_USER_NAME,
            password = config.DB_PASSWORD,
            host = config.DB_HOST,
            port = int(config.DB_PORT),
            database = config.DB_DATABASE
        )
             
    except mariadb.Error as e:
        conn = None
        print(f"Error connecting to MariaDB Platform: {e}")
    return conn

####### SCAN ########

def add_scan(scan_profile_id, engagment_id, jenkins_job_id, user_id, name, description, setup_date, status, schedule):
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (scan_profile_id, engagment_id, jenkins_job_id, user_id, name, description, setup_date, status, schedule,)
        procedure_name = 'sp_addScan'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("unable to add scan")
        
        scan_id = cursor.fetchone()[0]
                    
        cursor.close()       
    
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
    
    conn.commit()
    conn.close()
    return scan_id

def update_scan(scan_id, scan_profile_id, engagment_id, jenkins_job_id, user_id, name, description, setup_date, status, schedule):
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (scan_id, scan_profile_id, engagment_id, jenkins_job_id, user_id, name, description, setup_date, status, schedule)
        procedure_name = 'sp_updateScan'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("unable to update scan")
        
        cursor.close()       
    
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
    
    conn.commit()

def get_all_scan_by_product(product_id):
    result_set = []
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (product_id,)
        procedure_name = 'sp_get_scan_by_product'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("no scan found for product id : "+product_id)

        for c in cursor:
            result_set.append(c)
        
        cursor.close()
        
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
    
    conn.close()
    return result_set

def get_all_scan_by_component(component_id):
    result_set = []
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (component_id,)
        procedure_name = 'sp_getScanByComponent'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("no scan found for component id : "+component_id)

        for c in cursor:
            result_set.append(c)
        
        cursor.close()
        
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
    
    conn.close()
    return result_set

def get_scan(scan_id):
    result_set = []
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (scan_id,)
        procedure_name = 'sp_getScan'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("no scan found for scan id : "+scan_id)

        for c in cursor:
            result_set.append(c)
        
        cursor.close()
        
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
    
    conn.close()
    return result_set

def delete_scan(scan_id):
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (scan_id,)
        procedure_name = 'sp_deleteScan'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("no scan found of id : "+scan_id)
        
        print("successfuly deleted scan for id :"+str(scan_id))           
        cursor.close()       
    
    except mariadb.Error as e: 
        cursor.close()
        conn.close()
        raise MariadbError(str(e))
    
    conn.commit()
    conn.close()

    
#######  SCAN_TYPE  ########

def get_all_scan_types():
    result_set = []
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_name = 'sp_getAllScanTypes'
        
        cursor.callproc(procedure_name)
        if cursor.rowcount == 0:
            raise OperationError("no scan_type found")

        for c in cursor:
            result_set.append(c)
        
        cursor.close()
        
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        print(f"{e}")
        raise MariadbError("database internal error")
    
    conn.close()
    return result_set

def get_scan_type(scan_type_id):
    result_set = []
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (scan_type_id,)
        procedure_name = 'sp_getScanType'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("no scan_type found of id : "+scan_type_id)

        for c in cursor:
            result_set.append(c)
        
        cursor.close()
        
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
    
    conn.close()
    return result_set

def add_scan_type(name, description, jenkins_cfg_obj_name, scan_type_parameters=[]):
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (name, description,jenkins_cfg_obj_name,)
        procedure_name = 'sp_addScanType'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("unable to add scan Type")
        
        scan_type_id = cursor.fetchone()[0]
        
        for scan_type_parameter in scan_type_parameters:
            procedure_args = (scan_type_id, scan_type_parameter['name'], scan_type_parameter['description'])
            procedure_name = 'sp_addScanTypeParameter'
            cursor.callproc(procedure_name, procedure_args)
            if cursor.rowcount == 0:
                raise OperationError("unable to add scan Type parameter")
            
        cursor.close()       
    
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
    
    conn.commit()
    conn.close()
    return scan_type_id
    
def update_scan_type(scan_type_id, name, description, jenkins_cfg_obj_name, scan_Type_parameters=[]):
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (scan_type_id, name, description,jenkins_cfg_obj_name)
        procedure_name = 'sp_updateScanType'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("unable to update scan Type")
        
        for scan_Type_parameter in scan_Type_parameters:
            procedure_args = (scan_Type_parameter['id'], scan_Type_parameter['name'], scan_Type_parameter['description'])
            procedure_name = 'sp_updateScanTypeParameter'
            cursor.callproc(procedure_name, procedure_args)
            if cursor.rowcount == 0:
                raise OperationError("provided scan Type parameters not found for id:"+scan_type_id)
            
        cursor.close()       
    
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
        
    
    conn.commit()
    conn.close()

def delete_scan_type(scan_type_id):
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (scan_type_id,)
        procedure_name = 'sp_deleteScanType'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("no scan_type found of id : "+scan_type_id)
                   
        cursor.close()       
    
    except mariadb.Error as e: 
        cursor.close()
        conn.close()
        raise MariadbError(str(e))
    
    conn.commit()
    conn.close()

#######  SCAN_TYPE_PARAMETER  ########

def get_all_scan_type_parameters_of_scan_type(scan_type_id):
    result_set = []
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (scan_type_id,)
        procedure_name = 'sp_getScanTypeParameters'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("no scan_type_parameter found of scan_type id : "+scan_type_id)

        for c in cursor:
            result_set.append(c)
        
        cursor.close()
        
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
    
    conn.close()
    return result_set

def add_scan_type_parameters(scan_type_id, scan_type_parameters=[]):
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        for scan_type_parameter in scan_type_parameters:
            procedure_args = (scan_type_id, scan_type_parameter['name'], scan_type_parameter['description'])
            procedure_name = 'sp_addScanTypeParameter'
            cursor.callproc(procedure_name, procedure_args)
            if cursor.rowcount == 0:
                raise OperationError("unable to add scan Type parameter")
            
        cursor.close()       
    
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
        
    conn.commit()
    conn.close()

def update_scan_type_parameter(scan_type_parameter_id, name, description):
      conn = get_connection()
    
      if(not conn):
        raise ConnectionError("unable to connect to database")
    
      try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (scan_type_parameter_id, name, description)
        procedure_name = 'sp_updateScanTypeParameter'
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("provided scan Type parameter not found for id:"+scan_type_parameter_id)
            
        cursor.close()       
    
      except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
        
      conn.commit()
      conn.close()

def delete_scan_type_parameter(scan_type_parameter_id):
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (scan_type_parameter_id,)
        procedure_name = 'sp_deleteScanTypeParameter'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("no scan_type_parameter found of id : "+scan_type_parameter_id)
                   
        cursor.close()       
    
    except mariadb.Error as e: 
        cursor.close()
        conn.close()
        raise MariadbError(str(e))
    
    conn.commit()
    conn.close()
    
#######  SCAN_PROFILE ########

def update_scan_profile(scan_profile_id, name, description, scan_type_id, component_id, jenkins_cfg_obj_name=None, scan_parameters=[]):
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (scan_profile_id, name, description, scan_type_id, component_id, jenkins_cfg_obj_name)
        procedure_name = 'sp_updateScanProfile'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("unable to update scan profile")
        
        for scan_parameter in scan_parameters:
            procedure_args = (scan_profile_id, scan_parameter['name'], scan_parameter['value'])
            procedure_name = 'sp_updateScanProfileParameter'
            cursor.callproc(procedure_name, procedure_args)
            if cursor.rowcount == 0:
                raise OperationError("provided scan profile parameters not found for id:"+scan_profile_id)
            
        cursor.close()       
    
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")

    conn.commit()
    conn.close()
    
def add_scan_profile(name, description, scan_type_id, component_id, scan_parameters=[], jenkins_cfg_obj_name=None):
    
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (name, description, scan_type_id, component_id,jenkins_cfg_obj_name)
        procedure_name = 'sp_addScanProfile'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("unable to add scan profile")
        
        scan_profile_id = cursor.fetchone()[0]
        
        for scan_parameter in scan_parameters:
            procedure_args = (scan_profile_id, scan_parameter['name'], scan_parameter['value'])
            procedure_name = 'sp_addScanProfileParameter'
            cursor.callproc(procedure_name, procedure_args)
            if cursor.rowcount == 0:
                raise OperationError("unable to add scan profile parameter")
            
        cursor.close()
            
    
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
    
    conn.commit()
    conn.close()
    return scan_profile_id   

def delete_scan_profile(scan_profile_id):
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (scan_profile_id,)
        procedure_name = 'sp_deleteScanProfile'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("no scan_profile found of id : "+scan_profile_id)
                   
        cursor.close()       
    
    except mariadb.Error as e: 
        cursor.close()
        conn.close()
        raise MariadbError(str(e))
    
    conn.commit()
    conn.close()

def get_scan_profile(scan_profile_id):
    
    result_set = []
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (scan_profile_id,)
        procedure_name = 'sp_getScanProfile'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("no scan_profile found of id : "+scan_profile_id)

        for c in cursor:
            result_set.append(c)
        cursor.close()
        
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
    
    conn.close()
    return result_set

#######  SCAN_PROFILE_PARAMETER  ########

def get_all_scan_profile_parameters_of_scan_profile(scan_profile_id):
    result_set = []
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (scan_profile_id,)
        procedure_name = 'sp_getScanProfileParameters'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("no scan_profile_parameter found of scan_profile id : "+scan_profile_id)

        for c in cursor:
            result_set.append(c)
        
        cursor.close()
        
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
    
    conn.close()
    return result_set

def add_scan_profile_parameters(scan_profile_id, scan_profile_parameters=[]):
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        for scan_profile_parameter in scan_profile_parameters:
            procedure_args = (scan_profile_id, scan_profile_parameter['name'], scan_profile_parameter['value'])
            procedure_name = 'sp_addScanProfileParameter'
            cursor.callproc(procedure_name, procedure_args)
            if cursor.rowcount == 0:
                raise OperationError("unable to add scan Profile parameter")
            
        cursor.close()       
    
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
        
    conn.commit()
    conn.close()
    
def update_scan_profile_parameter(scan_profile_id, name, value):
      conn = get_connection()
    
      if(not conn):
        raise ConnectionError("unable to connect to database")
    
      try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (scan_profile_id, name, value)
        procedure_name = 'sp_updateScanProfileParameter'
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("provided scan Profile parameter not found for scan_profile_id id:"+scan_profile_id)
            
        cursor.close()       
    
      except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
        
      conn.commit()
      conn.close()
    
def delete_scan_profile_parameter(scan_profile_id, name):
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (scan_profile_id,name,)
        procedure_name = 'sp_deleteScanProfileParameter'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("no scan_profile_parameter found of name : "+name)
                   
        cursor.close()       
    
    except mariadb.Error as e: 
        cursor.close()
        conn.close()
        raise MariadbError(str(e))
    
    conn.commit()
    conn.close()

###### PRODUCT #######

def get_all_products():
    result_set = []
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_name = 'sp_getAllProducts'
        
        cursor.callproc(procedure_name)
        if cursor.rowcount == 0:
            raise OperationError("no products found")

        for c in cursor:
            result_set.append(c)
        
        cursor.close()
        
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        print(f"{e}")
        raise MariadbError("database internal error")
    
    conn.close()
    return result_set
    
def get_product(product_id):
    result_set = []
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (product_id,)
        procedure_name = 'sp_getproduct'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("no product found of id : "+product_id)

        for c in cursor:
            result_set.append(c)
        
        cursor.close()
        
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
    
    conn.close()
    return result_set
    
def add_product(name, description, user_id):
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (name, description, user_id)
        procedure_name = 'sp_addProduct'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("unable to add product")
        
        product_id = cursor.fetchone()[0]
            
        cursor.close()       
    
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
        
    conn.commit()
    conn.close()
    return product_id
    
def update_product(product_id, name, description):
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (product_id, name, description,)
        procedure_name = 'sp_updateProduct'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("unable to update product of id:"+product_id)
       
        cursor.close()       
    
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
    
    conn.commit()
    conn.close()
    
def delete_product(product_id):
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (product_id,)
        procedure_name = 'sp_deleteProduct'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("no product found of id : "+product_id)
                   
        cursor.close()       
    
    except mariadb.Error as e: 
        cursor.close()
        conn.close()
        raise MariadbError(str(e))
    
    conn.commit()
    conn.close()

###### COMPONENT ########

def get_all_components():
    result_set = []
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_name = 'sp_getAllComponents'
        
        cursor.callproc(procedure_name)
        if cursor.rowcount == 0:
            raise OperationError("no components found")

        for c in cursor:
            result_set.append(c)
        
        cursor.close()
        
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        print(f"{e}")
        raise MariadbError("database internal error")
    
    conn.close()
    return result_set

def get_component(component_id):
    result_set = []
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (component_id,)
        procedure_name = 'sp_getComponent'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("no components found of id : "+component_id)

        for c in cursor:
            result_set.append(c)
        
        cursor.close()
        
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
    
    conn.close()
    return result_set
    
def add_component(name, description, product_id):
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (name, description, product_id)
        procedure_name = 'sp_addComponent'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("unable to add component")
        
        component_id = cursor.fetchone()[0]
        
        cursor.close()       
    
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
        
    conn.commit()
    conn.close()
    return component_id

def update_component(component_id, name, description, product_id):
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (component_id, name, description, product_id,)
        procedure_name = 'sp_updateComponent'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("unable to update component")
 
        cursor.close()       
    
    except mariadb.Error as e:
        cursor.close()
        conn.close()
        raise MariadbError(f"{e}")
        
    conn.commit()
    conn.close()
    
def delete_component(component_id):
    conn = get_connection()
    
    if(not conn):
        raise ConnectionError("unable to connect to database")
    
    try:
        cursor = conn.cursor(buffered=True)
        
        procedure_args = (component_id,)
        procedure_name = 'sp_deleteComponent'
        
        cursor.callproc(procedure_name, procedure_args)
        if cursor.rowcount == 0:
            raise OperationError("no component found of id : "+component_id)
                   
        cursor.close()       
    
    except mariadb.Error as e: 
        cursor.close()
        conn.close()
        raise MariadbError(str(e))
    
    conn.commit()
    conn.close()

