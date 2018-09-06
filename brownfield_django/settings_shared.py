# flake8: noqa
# Django settings for brownfield_django project.
import os.path
from ccnmtlsettings.shared import common

project = 'brownfield_django'
base = os.path.dirname(__file__)
locals().update(common(project=project, base=base))

PROJECT_APPS = [
    'brownfield_django.main',
]

USE_TZ = True

TEMPLATES[0]['OPTIONS']['context_processors'].append(  # noqa
    'django.template.context_processors.csrf'
)

MIDDLEWARE += [  # noqa
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'brownfield_django.urls'

INSTALLED_APPS += [  # noqa
    'sorl.thumbnail',
    'rest_framework',
    'typogrify',
    'bootstrap3',
    'bootstrapform',
    'django_extensions',
    'crispy_forms',
    'registration',
    'pagetree',
    'pageblocks',
    'quizblock',
    'storages',
    'brownfield_django.main',
    'contactus'
]

PAGEBLOCKS = [
    'pageblocks.TextBlock',
    'pageblocks.HTMLBlock',
    'pageblocks.PullQuoteBlock',
    'pageblocks.ImageBlock',
    'pageblocks.ImagePullQuoteBlock',
    'quizblock.Quiz',
]

EMAIL_SUBJECT_PREFIX = "[brownfield] "

LOGIN_REDIRECT_URL = "/"

REGISTRATION_APPLICATION_MODEL = 'registration.Application'
ACCOUNT_ACTIVATION_DAYS = 7

REST_FRAMEWORK = {
    'DEFAULT_MODEL_SERIALIZER_CLASS':
    'rest_framework.serializers.ModelSerializer',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

ADMIN_AFFIL = 'tlc.cunix.local:columbia.edu'
DEBUG_TOOLBAR_PATCH_SETTINGS = False

SERVER_EMAIL = 'brownfield@ccnmtl.columbia.edu'
CONTACT_US_EMAIL = 'ctl-bfa@columbia.edu'