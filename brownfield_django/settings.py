# flake8: noqa
from brownfield_django.settings_shared import *

try:
    from browfield_django.local_settings import *
except ImportError:
    pass
