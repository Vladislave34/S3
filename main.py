import os
import boto3

#print("Сало - це смачно і дуже корисно!")
s3_client = boto3.client('s3') # S3 client


response = s3_client.list_buckets() # List all buckets
for bucket in response['Buckets']:
    print(bucket)

response = s3_client.list_objects_v2(Bucket='transferbucket21') # List objects in a bucket
objects = response.get('Contents', [])
print(objects)

s3_client.download_file("transferbucket21", "info.rtf", "downloaded_info.rtf") 

 
