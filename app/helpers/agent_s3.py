import logging
import boto3
import botocore
from app.config import S3_ACCESS_KEY_ID, S3_ACCESS_SECRET_KEY, S3_BUCKET_NAME, S3_LOCATION


s3_client = boto3.client(
    's3',
    aws_access_key_id=S3_ACCESS_KEY_ID,
    aws_secret_access_key=S3_ACCESS_SECRET_KEY
)


def upload_file_to_s3(file_obj, acl="public-read"):
    try:
        s3_client.upload_fileobj(file_obj, S3_BUCKET_NAME, str(file_obj.filename),
                                 ExtraArgs={"ACL": acl, "ContentType": file_obj.content_type})
    except Exception as e:
        print("Upload failed: ", e)
        return e
    return "{}{}".format(S3_LOCATION, file_obj.filename)
