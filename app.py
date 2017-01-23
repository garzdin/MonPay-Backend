from json import dumps
from falcon import API, HTTP_200
from models import db
from settings import DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME
from middleware.multipart import MultipartMiddleware
from controllers.account import *
from controllers.misc import *

__all__ = ['app']

db.bind('postgres', user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, database=DATABASE_NAME)
db.generate_mapping(create_tables=True)

app = API(middleware=[MultipartMiddleware()])
app.add_route('/api/v1/upload/file', FileUploadResource())
app.add_route('/api/v1/account/create', AccountCreateResource())
app.add_route('/api/v1/account/login', AccountLoginResource())
app.add_route('/api/v1/account/reset', AccountResetResource())
app.add_route('/api/v1/account/me', AccountResource())
