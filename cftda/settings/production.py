import random
import string
from .base import *

DEBUG = False

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'zm5&r%2jhd9b1w80#*_1ivztb)wcer4g585nny*ylu#5f=xe%f'
# generate a unique hash id and store it in query (for further query identification)
SECRET_KEY = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(32)).lower()

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGIN_REDIRECT_URL = '/admin'

# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# SECURE_SSL_REDIRECT = True

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

DEFAULT_FROM_EMAIL = 'tda@caltech.edu'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '[::1]', 'tda.caltech.edu',
                 '131.215.198.215', 'tda_server']
# ALLOWED_HOSTS = ['*']

try:
    from .local import *
except ImportError:
    pass
