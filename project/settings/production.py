from . import *
import dj_database_url

DEBUG = ENV("DEBUG", "0") == "1"

DEBUG_TOOLBAR = DEBUG

INSTALLED_APPS += []

try:
    DATABASES['default'] = dj_database_url.parse(os.environ.get('DATABASE_URL'))
    DATABASES['default']['ENGINE'] = os.environ.get(
        'DB_ENGINE', 'django.db.backends.postgresql_psycopg2')
except:
    pass

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', None)
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', None)
S3_USE_SIGV4 = True
AWS_IS_GZIPPED = True

if AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY and AWS_STORAGE_BUCKET_NAME:
    INSTALLED_APPS += ['storages']
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
