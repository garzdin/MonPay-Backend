from json import load, dumps
from datetime import datetime
from jwt import encode
from falcon import HTTPBadRequest, HTTPConflict, HTTPNotFound, HTTPForbidden, before
from settings import SECRET, TOKEN_EXPIRATION, TOKEN_ISSUER, TOKEN_AUDIENCE
from middleware.token import validate_token
from models.models import User, session

__all__ = ['UserCreateResource', 'UserLoginResource', 'UserRefreshResource',
           'UserResetResource', 'UserGetResource']


class UserCreateResource(object):
    def on_post(self, req, resp):
        """Handles POST requests"""
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if not 'email' in data or not 'password' in data:
            raise HTTPBadRequest(description="Email and password required")
        user = session.query(User).filter(User.email == data['email']).first()
        if user:
            raise HTTPConflict(description="Email already exists")
        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password'])
        session.add(user)
        session.commit()
        resp.body = dumps({"status": True, "user_id": user.id})


class UserLoginResource(object):
    def on_post(self, req, resp):
        """Handels POST requests"""
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if not 'email' in data or not 'password' in data:
            raise HTTPBadRequest(description="Email and password required")
        user = session.query(User).filter(User.email == data['email']).first()
        if not user:
            raise HTTPNotFound(description="Email not found")
        if not user.password == data['password']:
            raise HTTPForbidden(description="Incorrect password")
        token_data = {
            "iss": TOKEN_ISSUER,
            "aud": TOKEN_AUDIENCE,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + TOKEN_EXPIRATION,
            "uid": user.id
        }
        refresh_token_data = {
            "iss": TOKEN_ISSUER,
            "aud": TOKEN_AUDIENCE,
            "iat": datetime.utcnow(),
            "uid": user.id
        }
        token = encode(token_data, SECRET)
        refresh_token = encode(refresh_token_data, SECRET)
        resp.body = dumps({"status": True, "token": token.decode("utf-8"), "refresh_token": refresh_token.decode("utf-8")})


class UserRefreshResource(object):
    def on_post(self, req, resp):
        """Handles POST requests"""
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if not 'token' in data or not 'refresh_token' in data:
            raise HTTPBadRequest(description="Token and refresh token required")
        token = data['token']
        refresh_token = data['refresh_token']
        try:
            decoded = decode(refresh_token, SECRET, audience=TOKEN_AUDIENCE)
        except DecodeError as e:
            raise HTTPBadRequest(description="Could not decode refresh token")
        else:
            new_token_data = refresh_token
            new_token_data['exp'] = datetime.utcnow() + TOKEN_EXPIRATION
            new_token = encode(new_token_data, SECRET)
        resp.body = dumps({"status": True, "token": new_token.decode("utf-8"), "refresh_token": refresh_token})


class UserResetResource(object):
    def on_post(self, req, resp):
        """Handle POST requests"""
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if not 'email' in data:
            raise HTTPBadRequest(description="Email required")
        user = session.query(User).filter(User.email == data['email']).first()
        if not user:
            raise HTTPNotFound(description="Email not found")
        resp.body = dumps({"status": True})


class UserGetResource(object):
    @before(validate_token)
    def on_get(self, req, resp):
        user = session.query(User).get(req.uid)
        resp.body = dumps({"status": True, "user": {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "registered_on": str(user.created_on)
        }})
