# -*- coding: utf-8 -*-
import os

DEBUG=True
SASS_DEBUG = DEBUG
TEMPLATE_DEBUG=DEBUG
#COMPRESS_ENABLED=True
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

ADMINS = (
    ('jacek', 'jacek@ivolution.pl'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': "127.0.0.1",
        'PORT': '3306',
    },
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'email-smtp.us-east-1.amazonaws.com'
EMAIL_HOST_PASSWORD = ''
EMAIL_HOST_USER = 'AKIAIBZV3BA6HZSHI5BQ'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = ''

#ENV_PREFIX = 'styleguide-local'

ALLOWED_HOSTS = [
    'am.ivolution.pl',
    '127.0.0.1',
]

INTERNAL_IPS = (
    "127.0.0.1",
)
if SASS_DEBUG:
    COMPRESS_PRECOMPILERS = (
        #('text/x-scss', 'sass --scss  --debug-info {infile} {outfile}'),
        ('text/x-scss', 'sass --scss --compass  --debug-info {infile} {outfile}'),
    )
else:
    COMPRESS_PRECOMPILERS = (
        ('text/x-scss', 'sass --scss --compass {infile} {outfile}'),
    )