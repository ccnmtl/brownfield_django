# flake8: noqa
# Django settings for brownfield_django project.
import os.path
from ctlsettings.shared import common

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
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'brownfield_django.urls'

INSTALLED_APPS += [  # noqa
    'rest_framework',
    'typogrify',
    'bootstrap3',
    'bootstrapform',
    'django_extensions',
    'crispy_forms',
    'registration',
    'storages',
    'brownfield_django.main',
    'contactus',
    'markdownify.apps.MarkdownifyConfig',
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

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(base, "templates"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'stagingcontext.staging_processor',
                'gacontext.ga_processor',
            ],
        },
    },
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'
