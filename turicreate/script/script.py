import os
import turicreate as tc
import pandas as pd
from s3fs.core import S3FileSystem

import time
time.sleep(5) # Hacky way of avoiding having to check if the buckets have been created by docker.

os.environ['AWS_ACCESS_KEY_ID'] = 'minio'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'minio123'
os.environ['AWS_S3_ENDPOINT'] = 'http://minio:9000'

tc.config.set_runtime_config('TURI_S3_REGION', 'us-east-1')
tc.config.set_runtime_config('TURI_FILEIO_INSECURE_SSL_CERTIFICATE_CHECKS', 1)
tc.config.set_runtime_config('TURI_S3_ENDPOINT', 'http://minio:9000')

s3 = S3FileSystem(
    anon=False,
    client_kwargs={
        'endpoint_url':'http://minio:9000',
        'aws_access_key_id':'minio',
        'aws_secret_access_key':'minio123'
    })
location = 'output/sample.csv'

# This doesn't work because pandas can't read a private bucket
#df = pd.read_csv('s3://output/sample.csv')

# This does work as S3FileSystem is correctly configured for a private bucket
print('First getting the csv using S3FileSystem, and pandas...')
try:
    df = pd.read_csv(s3.open(location))
    print(df)
    print('Success')
except:
    print('ERROR: Couldnt get from S3 using pandas')
    raise


# This doesn't work and will error out despite the turicreate being configured to use the same parameters
print('\nNow try and get the same csv using Turicreate...')
try:
    sf = tc.SFrame.read_csv('s3://output/sample.csv')
    sf.print_rows()
    print('Success getting from S3 using Turicreate')
except:
    print('ERROR getting from S3 using turicreate')
    raise