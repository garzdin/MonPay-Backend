from datetime import timedelta

# The secret key used for signing tokens. Keep this safe.
SECRET = '1p294u3ejaskdnalkdu12ejan$spdokj+qe129u10emcn1hxemn1xz12ez1p9eu12'

# Database settings needed in order for the ORM to connect
DATABASE_USER = 'monpay'
DATABASE_PASSWORD = 'monpayPASS!'
DATABASE_HOST = 'localhost'
DATABASE_NAME = 'monpaydb'

# Token related settings
TOKEN_EXPIRATION = timedelta(hours=2)
TOKEN_ISSUER = 'MonPay Ltd.'
TOKEN_AUDIENCE = 'MonPay Client'
