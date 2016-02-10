# flake8: noqa
from settings_shared import *
from ccnmtlsettings.staging import common

locals().update(
    common(
        project=project,
        base=base,
        STATIC_ROOT=STATIC_ROOT,
        INSTALLED_APPS=INSTALLED_APPS,
    ))

AWS_STORAGE_BUCKET_NAME = 'ccnmtl-brownfield-static-stage'

try:
    from local_settings import *
except ImportError:
    pass
