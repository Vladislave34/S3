# import os
# import boto3
#
# #print("Сало - це смачно і дуже корисно!")
# s3_client = boto3.client('s3') # S3 client
#
#
# response = s3_client.list_buckets() # List all buckets
# for bucket in response['Buckets']:
#     print(bucket)
#
# response = s3_client.list_objects_v2(Bucket='transferbucket21') # List objects in a bucket
# objects = response.get('Contents', [])
# print(objects)
#
# s3_client.download_file("transferbucket21", "info.rtf", "downloaded_info.rtf")
# s3_client.put_bucket_versioning(
#     Bucket='transferbucket21',
#     VersioningConfiguration={'Status': 'Enabled'}
# ) # Enable versioning on a bucket
# response = s3_client.list_object_versions(
#     Bucket='transferbucket21',
#     Prefix='info.rtf'
# ) # List object versions in a bucket
#
# for version in response.get('Versions'):
#     print(version)
#
#
import os
import boto3
import subprocess
from datetime import datetime

# ====== CONFIG ======
DB_HOST = "3.79.255.104:5432"
DB_NAME = "transferbd"
DB_USER = "ivan"
DB_PASSWORD = "marko123halosh"

S3_BUCKET = "transferbucket21"

# ====================

# timestamp для імені файлу
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_file = f"backup_{DB_NAME}_{timestamp}.sql"

# 1️⃣ Робимо дамп БД
print("Creating database backup...")

os.environ["PGPASSWORD"] = DB_PASSWORD

dump_command = [
    "pg_dump",
    "-h", DB_HOST,
    "-U", DB_USER,
    "-F", "c",
    "-b",
    "-v",
    "-f", backup_file,
    DB_NAME
]

subprocess.run(dump_command, check=True)

print("Backup created:", backup_file)

# 2️⃣ Завантажуємо в S3
print("Uploading to S3...")

s3 = boto3.client("s3")
s3.upload_file(backup_file, S3_BUCKET, f"db_backups/{backup_file}")

print("Upload completed!")

# 3️⃣ Видаляємо локальний файл
os.remove(backup_file)

print("Local backup file removed.")