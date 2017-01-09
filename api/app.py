from json import load, dumps
from datetime import datetime, timedelta
from jwt import encode
from falcon import *
from middleware import validate_token
from models import *
from settings import *


db.bind('postgres', user=DATABASE_USER, password=DATABASE_PASSWORD, host=DATABASE_HOST, database=DATABASE_NAME)
db.generate_mapping(create_tables=True)


class IndexResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        resp.body = dumps({'message': "Welcome to the API!"})


class AccountCreateResource(object):
    @db_session
    def on_post(self, req, resp):
        """Handles POST requests"""
        data = load(req.bounded_stream)
        if not 'email' in data or not 'password' in data:
            raise falcon.HTTPBadRequest("Bad Request", "Email and password fields are required.")
        user = User.select(lambda u: u.email==data['email'])
        if user:
            raise falcon.HTTPConflict("Conflict", "A user with that email already exists.")
        user = User(
            first_name=data['first_name'] if 'first_name' in data else "",
            last_name=data['last_name'] if 'last_name' in data else "",
            email=data['email'],
            password=data['password']
        )
        resp.body = dumps({'message': "User created succeffully."})


class AccountLoginResource(object):
    @db_session
    def on_post(self, req, resp):
        """Handels POST requests"""
        data = load(req.bounded_stream)
        if not 'email' in data or not 'password' in data:
            raise falcon.HTTPBadRequest("Bad Request", "Email and password fields are required.")
        user = User.get(email=data['email'])
        if not user:
            raise falcon.HTTPNotFound("Not Found", "The user with the specified email was not found.")
        if not user.password == data['password']:
            raise falcon.HTTPForbidden("Forbidden", "The entered password is not correct.")
        token_data = {
            'iss': TOKEN_ISSUER,
            'aud': TOKEN_AUDIENCE,
            'iat': datetime.utcnow(),
            'uid': user.id
        }
        if not 'remember' in data:
            token_data['exp'] = datetime.utcnow() + TOKEN_EXPIRATION
        token = encode(token_data, SECRET)
        resp.body = dumps({'message': "Logged in succeffully.", 'token': token})


class AccountResource(object):
    @falcon.before(validate_token)
    @db_session
    def on_get(self, req, resp):
        if req.uid:
            user = User.get(id=req.uid)
            resp.body = dumps({
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'registered_on': str(user.created_on)
            })
        else:
            resp.body = dumps({'message': req.decode_error})


app = falcon.API()
app.add_route('/api/v1/', IndexResource())
app.add_route('/api/v1/account/create', AccountCreateResource())
app.add_route('/api/v1/account/login', AccountLoginResource())
app.add_route('/api/v1/account/me', AccountResource())
