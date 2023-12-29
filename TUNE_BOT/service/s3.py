import os

from conf.conf_s3 import client_s3


async def s3_upload(file_name, user_id):
    client_s3.Bucket(os.getenv('S3_BUCKET_ID')). \
        upload_file(f'media/{str(user_id)}/{file_name}',
                    f'tune/media/user/{str(user_id)}/{file_name}',
                    )
    os.remove(f'media/{user_id}/{file_name}')