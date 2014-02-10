"""
Django settings for sew_django project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os, datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

project = lambda: os.path.dirname(os.path.realpath(__file__))
location = lambda x: os.path.join(str(project()), str(x))

LOGIN_REDIRECT_URL="/profil/"
ADMIN_LOGIN_REDIRECT_URL="/admin/"

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
SERVER_EMAIL = 'jacek@ivolution.pl'
MANAGERS = ADMINS

# Application definition
COMPRESS_CSS_HASHING_METHOD = 'content'
COMPRESS_OFFLINE = True

AUTH_USER_MODEL = 'profiles.Profile'

PASSWORD_MIN_LENGTH = 8
PASSWORD_COMPLEXITY = { "UPPER":  1, "LOWER":  1, "DIGITS": 1 }

# Application definition

PROJECT_APPS = (
    # project
    'sew_django.profiles',
)

AUTHENTICATION_BACKENDS = (
    'sew_django.profiles.backends.EmailAuthBackend.EmailAuthBackend',
    'sew_django.profiles.backends.PeselAuthBackend.PeselAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
)


INSTALLED_APPS = (
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
    'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'passwords',
    'localflavor',
    'pyflakes',
    'sorl.thumbnail',
) + PROJECT_APPS

MIDDLEWARE_CLASSES = (
    'django.middleware.common.BrokenLinkEmailsMiddleware',#responsible of reporting 404 errors
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


ROOT_URLCONF = 'sew_django.urls'

WSGI_APPLICATION = 'sew_django.wsgi.application'

FORCE_SCRIPT_NAME = ""



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

LANGUAGE_CODE="pl"

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

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = location(os.path.join("site_media", "media"))

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/static/"

ADMIN_MEDIA_ROOT = location(os.path.join("static", "admin"))

TEMPLATE_DIRS = (
    location("templates"),
)

TINYMCE_SPELLCHECKER = False
TINYMCE_COMPRESSOR = False
TINYMCE_FILEBROWSER = True


FILEBROWSER_URL_FILEBROWSER_MEDIA = STATIC_URL + 'filebrowser/'
FILEBROWSER_PATH_FILEBROWSER_MEDIA = MEDIA_ROOT + 'filebrowser/'
FILEBROWSER_STATIC_URL = STATIC_URL + 'filebrowser/'

FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg', '.jpeg', '.gif', '.png'],
}
FILEBROWSER_VERSIONS_BASEDIR = '.thumbnails'
FILEBROWSER_URL_TINYMCE = STATIC_URL + "tiny_mce/"
FILEBROWSER_PATH_TINYMCE = STATIC_URL + "tiny_mce/"

FILEBROWSER_VERSIONS = {
                      'admin_thumbnail': {'verbose_name': 'Admin Thumbnail', 'width': 120, 'height': 120, 'opts': 'crop'},
                      }
FILEBROWSER_ADMIN_VERSIONS = []
FILEBROWSER_ADMIN_THUMBNAIL = 'admin_thumbnail'

COMPRESS_PRECOMPILERS = (
    #('text/x-scss', 'sass --scss  --debug-info {infile} {outfile}'),
    ('text/x-scss', 'sass --scss --compass  --debug-info {infile} {outfile}'),
)
today = datetime.date.today()
FINALE_NR = 22 + 2014 - today.year

if today.month > 1:
    #starting from february, we count for next year
    FINALE_NR = FINALE_NR + 1
try:
    from local_settings import *
except ImportError:
    print "no local_settings.py file?"

import sys
TESTING = ('test' in sys.argv)
TEST_CHARSET = 'utf8'

if TESTING:
    try:
        from test_settings import *        # pyflakes:ignore
        update_settings_for_tests(locals())
    except ImportError:
        pass

