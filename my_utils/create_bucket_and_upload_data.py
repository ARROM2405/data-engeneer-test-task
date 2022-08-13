import os.path
import time
import requests
from minio import Minio


def upload_data():
    access_key = 'minioadmin'
    secret_key = 'minioadmin'
    zip_upload_folder = 'source_data'
    trying = None
    try:
        for file in os.listdir(zip_upload_folder):
            print(file)
            if file.endswith('.zip'):
                print(f'adding file {file}')
                zip_upload_path = os.path.join(zip_upload_folder, file)
                print(zip_upload_path)
                break
        trying = True
    except:
        print('no such file or directory')
        trying = False
    minio_client = Minio('minio:9000', access_key=access_key, secret_key=secret_key, secure=False)
    a = 0
    while trying:
        a += 1
        try:
            minio_client.make_bucket(bucket_name='processed-data')
        except:
            pass
        try:
            minio_client.make_bucket(bucket_name='source')
        except:
            pass
        try:
            minio_client.fput_object('source', 'source.zip', zip_upload_path)
            print(f'added {zip_upload_path}')
            trying = False
        except Exception as e:
            time.sleep(5)
            print(e)


def update_request():
    while True:
        try:
            requests.post('http://django-app:8000/data/', json={
                "my_user_id": "",
                "first_name": "",
                "last_name": "",
                "births": "",
                "user_image_path": ""
            })
            print('updated data')
            time.sleep(60 * 55)
        except:
            print('could not update data')
            time.sleep(10)


upload_data()
time.sleep(2)
update_request()
