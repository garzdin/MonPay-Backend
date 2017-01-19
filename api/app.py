from json import dumps
from falcon import API, HTTP_200
import stripe
from models import db
from settings import DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME, STRIPE_API_KEY
from controllers import *

__all__ = ['app']

db.bind('postgres', user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, database=DATABASE_NAME)
db.generate_mapping(create_tables=True)

stripe.api_key = STRIPE_API_KEY

app = API()
app.add_route('/api/v1/account/create', AccountCreateResource())
app.add_route('/api/v1/account/login', AccountLoginResource())
app.add_route('/api/v1/account/reset', AccountResetResource())
app.add_route('/api/v1/account/me', AccountResource())
