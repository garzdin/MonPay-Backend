from json import load, dumps
from datetime import datetime
from jwt import encode
from falcon import HTTPBadRequest, HTTPConflict, HTTPNotFound, HTTPForbidden, before
from ..settings import SECRET, TOKEN_EXPIRATION, TOKEN_ISSUER, TOKEN_AUDIENCE
from ..middlewares import validate_token
from ..models import db_session, User
from ..app import stripe

__all__ = ['AccountCreateResource', 'AccountCreateSpecsResource',
           'AccountLoginResource', 'AccountResetResource',
           'AccountResource']


class AccountCreateSpecsResource(object):
    def on_get(self, req, resp):
        """Handles GET requests"""
        params = req.params
        if 'country' not in params:
            raise HTTPBadRequest(description="Country code required", code=1)
        country = params['country']
        spec = stripe.CountrySpec.retrieve(country)
        fields = spec['verification_fields']['individual']
        resp.body = dumps({"sepc": fields})


class AccountCreateResource(object):
    @db_session
    def on_post(self, req, resp):
        """Handles POST requests"""
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request", code=1)
        if not 'email' in data or not 'password' in data:
            raise HTTPBadRequest(description="Email and password required", code=1)
        user = User.select(lambda u: u.email == data['email'])
        if user:
            raise HTTPConflict(description="Email already exists", code=1)
        if not 'first_name' in data or not 'last_name' in data or not 'type' or not 'country' in data or not 'address' in data or not 'dob' in data or not 'tos_acceptance' in data:
            raise HTTPBadRequest(description="Some requried fields were not completed", code=1)
        legal_entity = {
            "first_name": data['first_name'],
            "last_name": data['last_name'],
            "type": data['type'],
            "address": {
                "city": data['address']['city'],
                "line1": data['address']['line1'],
                "postal_code": data['address']['postal_code']
            },
            "dob": {
                "day": data['dob']['day'],
                "month": data['dob']['month'],
                "year": data['dob']['year']
            }
        }
        tos_acceptance = {
            "date": data['tos_acceptance']['date'],
            "ip": data['tos_acceptance']['ip']
        }
        stripe_account = stripe.Account.create(
            managed=True,
            country=data['country'],
            email=data['email'],
            legal_entity=legal_entity,
            tos_acceptance=tos_acceptance
        )
        user = User(
            stripe_id=stripe_account['id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=data['password']
        )
        resp.body = dumps({"description": "User created succeffully", })


class AccountLoginResource(object):
    @db_session
    def on_post(self, req, resp):
        """Handels POST requests"""
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request", code=1)
        if not 'email' in data or not 'password' in data:
            raise HTTPBadRequest(description="Email and password required", code=1)
        user = User.get(email=data['email'])
        if not user:
            raise HTTPNotFound(description="Email not found", code=1)
        if not user.password == data['password']:
            raise HTTPForbidden(description="Incorrect password", code=2)
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


class AccountResetResource(object):
    @db_session
    def on_post(self, req, resp):
        """Handle POST requests"""
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request", code=1)
        if not 'email' in data:
            raise HTTPBadRequest(description="Email required", code=1)
        user = User.get(email=data['email'])
        if not user:
            raise HTTPNotFound(description="Email not found", code=1)
        resp.body = dumps({"message": "Email sent", "status": "success"})


class AccountResource(object):
    @before(validate_token)
    @db_session
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
