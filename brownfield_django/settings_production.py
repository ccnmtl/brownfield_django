from django.conf import settings
from brownfield_django.settings_shared import *  # noqa: F403
from ctlsettings.production import common, init_sentry

locals().update(
    common(
        project=project,  # noqa: F405
        base=base,  # noqa: F405
        INSTALLED_APPS=INSTALLED_APPS,  # noqa: F405
        STATIC_ROOT=STATIC_ROOT,  # noqa: F405
        s3prefix='ccnmtl',
    ))

AWS_STORAGE_BUCKET_NAME = 'ccnmtl-brownfield-static-prod'
S3_URL = 'https://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = ('https://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME)
MEDIA_URL = S3_URL + 'uploads/'
COMPRESS_URL = STATIC_URL

try:
    from brownfield_django.local_settings import *  # noqa: F403
except ImportError:
    pass

if hasattr(settings, 'SENTRY_DSN'):
    init_sentry(SENTRY_DSN)  # noqa F405
