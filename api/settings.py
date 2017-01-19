from os import environ
from datetime import timedelta

# The secret key used for signing tokens. Keep this safe.
SECRET = '1p294u3ejaskdnalkdu12ejan$spdokj+qe129u10emcn1hxemn1xz12ez1p9eu12'

# The API key to use when making calls to Stripe
STRIPE_API_KEY = "sk_test_yDWzXT12gNqPiJYmICXNd4Vw"

# Database settings needed in order for the ORM to connect
if 'DATABASE_URL' in environ:
    DATABASE_BASE_URL = environ['DATABASE_URL'].split('//')[1].split(':')
    DATABASE_USER = DATABASE_BASE_URL[0]
    DATABASE_PASSWORD = DATABASE_BASE_URL[1].split('@')[0]
    DATABASE_HOST = DATABASE_BASE_URL[1].split('@')[1]
    DATABASE_NAME = DATABASE_BASE_URL[2].split('/')[1]
else:
    DATABASE_USER = 'monpay'
    DATABASE_PASSWORD = 'monpayPASS!'
    DATABASE_HOST = 'localhost'
    DATABASE_NAME = 'monpaydb'

# Token related settings
TOKEN_EXPIRATION = timedelta(hours=2)
TOKEN_ISSUER = 'MonPay Ltd.'
TOKEN_AUDIENCE = 'MonPay Client'
