from .default import *
import dj_database_url

DEBUG = False
DEBUG_TOOLBAR = False

INSTALLED_APPS += []

try:
	DATABASES['default'] =  dj_database_url.parse(os.environ.get('DATABASE_URL'))
	DATABASES['default']['ENGINE'] = os.environ.get('DB_ENGINE', 'django.db.backends.postgresql_psycopg2')
except:
	pass

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'