from json import load, dumps
from datetime import datetime
from jwt import encode
from falcon import HTTPBadRequest, HTTPConflict, HTTPNotFound, HTTPForbidden, before
from settings import SECRET, TOKEN_EXPIRATION, TOKEN_ISSUER, TOKEN_AUDIENCE
from middleware.token import validate_token
from models import User, session

__all__ = ['UserCreateResource', 'UserLoginResource',
           'UserResetResource', 'UserResource']


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
            password=data['password']
        )
        session.add(user)
        session.commit()
        resp.body = dumps({
            "status": "success",
            "user_id": user.id
        })


class UserLoginResource(object):
    def on_post(self, req, resp):
        """Handels POST requests"""
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if not 'email' in data or not 'password' in data:
            raise HTTPBadRequest(description="Email and password required")
        user = User.get(email=data['email'])
        if not user:
            raise HTTPNotFound(description="Email not found")
        if not user.password == data['password']:
            raise HTTPForbidden(description="Incorrect password")
        token_data = {
            "iss": TOKEN_ISSUER,
            "aud": TOKEN_AUDIENCE,
            "iat": datetime.utcnow(),
            "uid": user.id
        }
        if not 'remember' in data:
            token_data['exp'] = datetime.utcnow() + TOKEN_EXPIRATION
        token = encode(token_data, SECRET)
        resp.body = dumps({"message": "Logged in succeffully", "token": token})


class UserResetResource(object):
    def on_post(self, req, resp):
        """Handle POST requests"""
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if not 'email' in data:
            raise HTTPBadRequest(description="Email required")
        user = User.get(email=data['email'])
        if not user:
            raise HTTPNotFound(description="Email not found")
        resp.body = dumps({"message": "Email sent", "status": "success"})


class UserResource(object):
    @before(validate_token)
    def on_get(self, req, resp):
        if req.uid:
            user = User.get(id=req.uid)
            resp.body = dumps({
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "registered_on": str(user.created_on)
            })
        else:
            resp.body = dumps({"message": req.decode_error})
