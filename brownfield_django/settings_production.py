# flake8: noqa
from settings_shared import *

TEMPLATE_DIRS = (
    "/var/www/brownfield_django/brownfield_django/brownfield_django/templates",
)

MEDIA_ROOT = '/var/www/brownfield_django/uploads/'
# put any static media here to override app served static media
STATICMEDIA_MOUNTS = (
    ('/sitemedia', '/var/www/brownfield_django/brownfield_django/sitemedia'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'brownfield_django',
        'HOST': '',
        'PORT': 6432,
        'USER': '',
        'PASSWORD': '',
    }
}

COMPRESS_ROOT = "/var/www/brownfield_django/brownfield_django/media/"
DEBUG = False
TEMPLATE_DEBUG = DEBUG
DEBUG_TOOLBAR_PATCH_SETTINGS = False
# I don't see this setting in NEPI's prod settings so taking it out
# SENTRY_SITE = 'brownfield_django'
SENTRY_SERVERS = ['http://sentry.ccnmtl.columbia.edu/sentry/store/']

if 'migrate' not in sys.argv:
    INSTALLED_APPS.append('raven.contrib.django.raven_compat')

try:
    from local_settings import *
except ImportError:
    pass
