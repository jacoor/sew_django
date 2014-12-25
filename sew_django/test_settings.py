import os
TEST_DATABASE_CHARSET = 'utf8'


def update_settings_for_tests(settings):
    """Modify some of the values set in settings.py.
    """

    if getattr(settings, '_settings_updated', None):
        return
    settings['_settings_updated'] = True
    settings['BROKER_BACKEND'] = 'memory'
    settings['COMPRESS_PRECOMPILERS'] = []

    settings['PASSWORD_HASHERS'] = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
        'django.contrib.auth.hashers.SHA1PasswordHasher',
    )

    print "Warning: disabling cache middleware for the duration of unit tests"
    settings['MIDDLEWARE_CLASSES'] = [mc
                                      for mc in settings['MIDDLEWARE_CLASSES']
                                      if 'CacheMiddleware' not in mc]

    if os.getenv('FASTER'):
        settings['DATABASES'] = {
            'default': {
                'NAME': ':memory:',
                'ENGINE': 'django.db.backends.sqlite3',
            },
        }
