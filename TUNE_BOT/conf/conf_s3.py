import os

import boto3

client_s3 = boto3.resource(
    service_name='s3',
    aws_access_key_id=os.getenv('S3_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('S3_SECRET_ACCESS_KEY'),
    endpoint_url=os.getenv('S3_ENDPOINT_URL'),

)
