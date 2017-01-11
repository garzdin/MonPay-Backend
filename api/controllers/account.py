from json import load, dumps
from datetime import datetime
from jwt import encode
from falcon import HTTPBadRequest, HTTPConflict, HTTPNotFound, HTTPForbidden, before
from settings import SECRET, TOKEN_EXPIRATION, TOKEN_ISSUER, TOKEN_AUDIENCE
from middlewares import validate_token
from models import db_session, User

__all__ = ['AccountCreateResource', 'AccountLoginResource', 'AccountResource']

class AccountCreateResource(object):
    @db_session
    def on_post(self, req, resp):
        """Handles POST requests"""
        data = load(req.bounded_stream)
        if not 'email' in data or not 'password' in data:
            raise HTTPBadRequest("Bad Request", "Email and password fields are required.")
        user = User.select(lambda u: u.email==data['email'])
        if user:
            raise HTTPConflict("Conflict", "A user with that email already exists.")
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
            raise HTTPBadRequest("Bad Request", "Email and password fields are required.")
        user = User.get(email=data['email'])
        if not user:
            raise HTTPNotFound("Not Found", "The user with the specified email was not found.")
        if not user.password == data['password']:
            raise HTTPForbidden("Forbidden", "The entered password is not correct.")
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
    @before(validate_token)
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
