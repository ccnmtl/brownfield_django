# flake8: noqa
from brownfield_django.settings_shared import *
from ccnmtlsettings.docker import common
import os

locals().update(
    common(
        project=project,
        base=base,
        STATIC_ROOT=STATIC_ROOT,
        INSTALLED_APPS=INSTALLED_APPS,
    ))
