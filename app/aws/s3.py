import boto3

def download_file(bucketname, src_file_path, des_file_path):
    s3=boto3.resource('s3')
    s3.Bucket(bucketname).download_file(src_file_path, des_file_path)
    
def upload_file(bucketname, src_file_path, des_file_path):
    s3 = boto3.resource('s3')
    s3.Object(bucketname, des_file_path).upload_file(src_file_path)
    