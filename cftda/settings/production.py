import random
import string
from .base import *

DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zm5&r%2jhd9b1w80#*_1ivztb)wcer4g585nny*ylu#5f=xe%f'
# generate a unique hash id and store it in query (for further query identification)
# SECRET_KEY = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32)).lower()

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join('/cftda-db', 'db.sqlite3'),
        }
    }

MEDIA_ROOT = '/cftda-media'

LOGIN_REDIRECT_URL = '/admin'

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

DEFAULT_FROM_EMAIL = 'tda@caltech.edu'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0', '[::1]', 'tda.caltech.edu',
                 '131.215.198.215', 'tda_server', '192.168.31.157', 'rico.caltech.edu']
# ALLOWED_HOSTS = ['*']

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# SECURE_SSL_REDIRECT = True

try:
    from .local import *
except ImportError:
    pass
