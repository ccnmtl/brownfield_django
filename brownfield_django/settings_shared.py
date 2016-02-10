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

TEMPLATE_CONTEXT_PROCESSORS += [  # noqa
    'django.template.context_processors.csrf'
]

MIDDLEWARE_CLASSES += [  # noqa
    'django.middleware.csrf.CsrfViewMiddleware',
]

ROOT_URLCONF = 'brownfield_django.urls'

INSTALLED_APPS += [  # noqa
    'sorl.thumbnail',
    'tagging',
    'rest_framework',
    'typogrify',
    'bootstrapform',
    'django_extensions',
    'crispy_forms',
    'registration',
    'pagetree',
    'pageblocks',
    'quizblock',
    'storages',
    'brownfield_django.main',
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
SERVER_EMAIL = 'ccnmtl-bfa@columbia.edu'
DEFAULT_FROM_EMAIL = SERVER_EMAIL

LOGIN_REDIRECT_URL = "/"

REGISTRATION_APPLICATION_MODEL = 'registration.Application'
MIGRATION_MODULES = {
    'registration': 'brownfield_django.migrations.registration',
}
ACCOUNT_ACTIVATION_DAYS = 7

REST_FRAMEWORK = {
    'DEFAULT_MODEL_SERIALIZER_CLASS':
    'rest_framework.serializers.ModelSerializer',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

