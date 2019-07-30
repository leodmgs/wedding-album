from os import urandom, environ

S3_BUCKET_NAME = "wedding-app-images"
S3_ACCESS_KEY_ID = environ.get('S3_ACCESS_KEY_ID')
S3_ACCESS_SECRET_KEY = environ.get('S3_ACCESS_SECRET_KEY')
S3_LOCATION = 'https://{}.s3-sa-east-1.amazonaws.com/'.format(S3_BUCKET_NAME)

SECRET_KEY = urandom(32)
DEBUG = True
API_ADDRESS = "https://enigmatic-mountain-68956.herokuapp.com"
PORT = 5000
