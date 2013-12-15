"""
Django settings for sew_django project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

project = lambda: os.path.dirname(os.path.realpath(__file__))
location = lambda x: os.path.join(str(project()), str(x))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vh@yfr%59d7v%81ovor+2j^s(ra8s32pd89n%gf0i%v0si+$8^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['am.ivolution.pl']


ADMINS = (
    ('jacek', 'jacek@ivolution.pl'),
)

MANAGERS = ADMINS

# Application definition
COMPRESS_CSS_HASHING_METHOD = 'content'
COMPRESS_OFFLINE = True

AUTH_USER_MODEL = 'profiles.Profile'

# Application definition

PROJECT_APPS = (
    # project
    'sew_django.profiles',
)


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'south',
    'ydcommon',
    'tinymce',
    'compressor',
    'raven.contrib.django.raven_compat',
) + PROJECT_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'sew_django.urls'

WSGI_APPLICATION = 'sew_django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '3306',
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = location(os.path.join("site_media", "static"))

# Additional directories which hold static files
STATICFILES_DIRS = [
    location("static"),
]

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

TEMPLATE_DIRS = (
    location("templates"),
)

COMPRESS_PRECOMPILERS = (
    #('text/x-scss', 'sass --scss  --debug-info {infile} {outfile}'),
    ('text/x-scss', 'sass --scss --compass  --debug-info {infile} {outfile}'),
)

try:
    from local_settings import *
except ImportError:
    print "no local_settings.py file?"
