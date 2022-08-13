import csv
from io import TextIOWrapper
from zipfile import ZipFile

from django.utils.timezone import now
from minio import Minio
import os
import shutil
from provectus_app.models import *


def update_data():
    update = False
    last_update = LastUpdate.objects.get_or_create(pk=1)
    last_update_date = last_update[0].last_update
    access_key = 'minioadmin'
    secret_key = 'minioadmin'
    minio_client = Minio('minio:9000', access_key=access_key, secret_key=secret_key, secure=False)
    bucket_name = 'source'
    zip_template_path = 'minio_data/minio_template.zip'
    zip_download_path = 'minio_data/minio.zip'
    os.remove(zip_download_path)
    shutil.copy(zip_template_path, zip_download_path)
    output_csv_path = 'minio_data/output.csv'

    for item in minio_client.list_objects(bucket_name):
        try:
            if item.last_modified > last_update_date:
                update = True
        except TypeError:
            update = True

        if update:
            minio_client.fget_object(bucket_name=bucket_name, object_name=item.object_name,
                                     file_path=zip_download_path)

    if update:
        print('processing')
        db_ids = [obj.my_user_id for obj in UserData.objects.all()]
        with ZipFile(zip_download_path) as zf:
            for file_archived in zf.filelist:
                if not file_archived.filename.startswith('__'):
                    object_id = os.path.basename(file_archived.filename).split('.')[0]
                    if object_id in db_ids:
                        db_ids.pop(db_ids.index(object_id))
                    model_instance = UserData.objects.get_or_create(my_user_id=object_id)[0]

                    if file_archived.filename.endswith('.csv'):
                        with zf.open(file_archived, 'r') as infile:
                            reader = csv.reader(TextIOWrapper(infile, 'utf-8'))
                            data_row = list(reader)[1]
                            first_name = data_row[0]
                            last_name = data_row[1]
                            births = data_row[2]
                            model_instance.first_name = first_name
                            model_instance.last_name = last_name
                            model_instance.births = births
                            model_instance.save()

                    elif file_archived.filename.endswith('.png'):
                        model_instance.user_image_path = f'{bucket_name}/{os.path.basename(file_archived.filename)}'
                        model_instance.save()
            if len(db_ids) > 0:
                UserData.objects.filter(my_user_id__in=db_ids).delete()
        csv_file = open(output_csv_path, 'w')
        writer = csv.writer(csv_file)
        for obj in UserData.objects.all():
            if obj.my_user_id and obj.my_user_id != '':
                write_row = [obj.my_user_id, obj.first_name, obj.last_name]
                if obj.user_image_path:
                    write_row.append(obj.user_image_path)
                writer.writerow(write_row)
        csv_file.close()
        minio_client.fput_object('processed-data', 'output.csv', output_csv_path, )
    else:
        print('not processing')
    db_update = LastUpdate.objects.get_or_create(pk=1)[0]
    db_update.last_update = now()
    db_update.save()
