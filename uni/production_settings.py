import dj_database_url
from .settings import *

DATABASES = {
    'defaults': dj_database_url.config(),
}
STATIC_ROOT = 'staticfiles'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']
DEBUG = False