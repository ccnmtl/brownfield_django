# flake8: noqa
from brownfield_django.settings_shared import *
from ctlsettings.compose import common

locals().update(
    common(
        project=project,
        base=base,
        STATIC_ROOT=STATIC_ROOT,
        INSTALLED_APPS=INSTALLED_APPS,
        s3prefix='ccnmtl',
    ))

try:
    from brownfield_django.local_settings import *
except ImportError:
    pass
