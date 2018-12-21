# flake8: noqa
from brownfield_django.settings_shared import *
from ccnmtlsettings.staging import common

locals().update(
    common(
        project=project,
        base=base,
        STATIC_ROOT=STATIC_ROOT,
        INSTALLED_APPS=INSTALLED_APPS,
    ))

AWS_STORAGE_BUCKET_NAME = 'ccnmtl-brownfield-static-stage'
S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = ('https://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME)
MEDIA_URL = S3_URL + 'uploads/'
COMPRESS_URL = STATIC_URL

try:
    from brownfield_django.local_settings import *
except ImportError:
    pass
