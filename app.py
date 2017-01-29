from json import dumps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from falcon import API, HTTP_200
from utils.db import construct_url
from settings import DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME
from middleware.multipart import MultipartMiddleware
from controllers.user import *
from controllers.misc import *

__all__ = ['app', 'session']

engine = create_engine(construct_url('postgres', DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_NAME))
session = sessionmaker(bind=engine)()

app = API(middleware=[MultipartMiddleware()])
app.add_route('/api/v1/upload/file', FileUploadResource())
app.add_route('/api/v1/user/create', UserCreateResource())
app.add_route('/api/v1/user/login', UserLoginResource())
app.add_route('/api/v1/user/reset', UserResetResource())
app.add_route('/api/v1/user/me', UserResource())
