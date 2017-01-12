from json import dumps
from falcon import API, HTTP_200
from models import db
from settings import DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME
from controllers import *

__all__ = ['app']

db.bind('postgres', user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, database=DATABASE_NAME)
db.generate_mapping(create_tables=True)


class IndexResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = HTTP_200
        resp.body = dumps({'message': "Welcome to the API!"})

app = API()
app.add_route('/api/v1/', IndexResource())
app.add_route('/api/v1/account/create', AccountCreateResource())
app.add_route('/api/v1/account/login', AccountLoginResource())
app.add_route('/api/v1/account/reset', AccountResetResource())
app.add_route('/api/v1/account/me', AccountResource())
