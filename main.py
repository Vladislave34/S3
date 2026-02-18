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
import subprocess
import boto3
from datetime import datetime
import gzip
import shutil

# ===== CONFIG =====
import os
import subprocess
import boto3
from datetime import datetime
import gzip
import shutil

# ===== CONFIG =====
CONTAINER_ID = "283995e8d7a6"  # ID контейнера
DB_NAME = "transferbd"
DB_USER = "ivan"
DB_PASSWORD = "marko123halosh"
S3_BUCKET = "transferbucket21"

BACKUP_DIR = "/tmp/db_backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
backup_filename = f"{DB_NAME}_{timestamp}.sql"
backup_path = os.path.join(BACKUP_DIR, backup_filename)
compressed_path = backup_path + ".gz"

print("Creating database backup inside container...")

# Використовуємо ID контейнера
dump_command = f'docker exec -e PGPASSWORD={DB_PASSWORD} {CONTAINER_ID} pg_dump -U {DB_USER} -F c {DB_NAME}'

# Виконуємо pg_dump і записуємо у файл
with open(backup_path, "wb") as f:
    subprocess.run(dump_command, shell=True, check=True, stdout=f)

print("Compressing backup...")

with open(backup_path, "rb") as f_in:
    with gzip.open(compressed_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)

os.remove(backup_path)

print("Uploading to S3...")

s3 = boto3.client("s3")
s3_key = f"docker-postgres-backups/{datetime.now().strftime('%Y/%m/%d')}/{os.path.basename(compressed_path)}"
s3.upload_file(compressed_path, S3_BUCKET, s3_key)

os.remove(compressed_path)

print("Backup completed and uploaded:", s3_key)