from os import environ
from datetime import timedelta

# The secret key used for signing tokens. Keep this safe.
SECRET = '1p294u3ejaskdnalkdu12ejan$spdokj+qe129u10emcn1hxemn1xz12ez1p9eu12'

# Database settings needed in order for the ORM to connect
if 'DEBUG' in environ:
    DATABASE_USER = 'monpay'
    DATABASE_PASSWORD = 'monpayPASS!'
    DATABASE_HOST = 'postgres'
    DATABASE_NAME = 'monpaydb'
else:
    DATABASE_BASE_URL = environ.get('DATABASE_URL').split('//')[1].split(':')
    DATABASE_USER = DATABASE_BASE_URL[0]
    DATABASE_PASSWORD = DATABASE_BASE_URL[1].split('@')[0]
    DATABASE_HOST = DATABASE_BASE_URL[1].split('@')[1]
    DATABASE_NAME = DATABASE_BASE_URL[2].split('/')[1]

# Token related settings
TOKEN_EXPIRATION = timedelta(hours=1)
REFRESH_TOKEN_EXPIRATION = timedelta(days=7)
TOKEN_ISSUER = 'MonPay Ltd.'
TOKEN_AUDIENCE = 'MonPay Client'
