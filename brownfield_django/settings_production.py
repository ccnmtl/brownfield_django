# flake8: noqa
from brownfield_django.settings_shared import *
from ccnmtlsettings.production import common

locals().update(
    common(
        project=project,
        base=base,
        INSTALLED_APPS=INSTALLED_APPS,
        STATIC_ROOT=STATIC_ROOT,
    ))

AWS_STORAGE_BUCKET_NAME = 'ccnmtl-brownfield-static-prod'
S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = ('https://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME)
MEDIA_URL = S3_URL + 'uploads/'
COMPRESS_URL = STATIC_URL

try:
    from brownfield_django.local_settings import *
except ImportError:
    pass
