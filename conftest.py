from django.conf import settings
import base64
import os
import os.path


def pytest_configure(config):
    import warnings
    warnings.filterwarnings('error', '', Warning, r'(sentry|raven)')

    if not settings.configured:
        os.environ['DJANGO_SETTINGS_MODULE'] = 'sentry.conf.server'

    test_db = os.environ.get('DB', 'sqlite')
    if test_db == 'mysql':
        settings.DATABASES['default'].update({
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'sentry',
            'USER': 'root',
        })
    elif test_db == 'postgres':
        settings.DATABASES['default'].update({
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': 'postgres',
            'NAME': 'sentry',
            'OPTIONS': {
                'autocommit': True,
            }
        })
    elif test_db == 'sqlite':
        settings.DATABASES['default'].update({
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        })

    # http://djangosnippets.org/snippets/646/
    class InvalidVarException(object):
        def __mod__(self, missing):
            try:
                missing_str = unicode(missing)
            except:
                missing_str = 'Failed to create string representation'
            raise Exception('Unknown template variable %r %s' % (missing, missing_str))

        def __contains__(self, search):
            if search == '%s':
                return True
            return False

    settings.TEMPLATE_DEBUG = True
    # settings.TEMPLATE_STRING_IF_INVALID = InvalidVarException()

    # Disable static compiling in tests
    settings.STATIC_BUNDLES = {}

    # override a few things with our test specifics
    settings.INSTALLED_APPS = tuple(settings.INSTALLED_APPS) + (
        'tests',
    )
    settings.SENTRY_KEY = base64.b64encode(os.urandom(40))
    settings.SENTRY_PUBLIC = False
    # This speeds up the tests considerably, pbkdf2 is by design, slow.
    settings.PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]

    # enable draft features
    settings.SENTRY_ENABLE_EXPLORE_CODE = True
    settings.SENTRY_ENABLE_EXPLORE_USERS = True


_HAS_FIXED_SEQUENCES = False


def pytest_runtest_call(item):
    # HACK: sequences arent reset for postgres
    global _HAS_FIXED_SEQUENCES

    if not _HAS_FIXED_SEQUENCES:
        import os

        os.environ['DJANGO_COLORS'] = 'nocolor'

        from django.core.management import call_command
        from django.conf import settings
        from django.db import connection
        from django.db.models.loading import get_app
        from StringIO import StringIO

        commands = StringIO()
        cursor = connection.cursor()

        for app in settings.INSTALLED_APPS:
            label = app.split('.')[-1]
            if get_app(label, emptyOK=True):
                call_command('sqlsequencereset', label, stdout=commands)

        value = commands.getvalue()
        if value:
            cursor.execute(value)

        _HAS_FIXED_SEQUENCES = True
