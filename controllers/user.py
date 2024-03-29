from json import load, dumps
from datetime import datetime
from jwt import encode, decode, ExpiredSignatureError, DecodeError
from falcon import HTTPBadRequest, HTTPConflict, HTTPNotFound, HTTPForbidden, before
from settings import SECRET, TOKEN_EXPIRATION, REFRESH_TOKEN_EXPIRATION, TOKEN_ISSUER, TOKEN_AUDIENCE
from middleware.token import validate_token
from encoders.datetime import DateTimeEncoder
from models.models import User, Address, session
from models.schema import UserSchema, AddressSchema

__all__ = ['UserCreateResource', 'UserLoginResource', 'UserRefreshResource',
           'UserResetResource', 'UserGetResource', 'UserUpdateResource',
           'UserAddressResource']


class UserCreateResource(object):
    def on_post(self, req, resp):
        """Handles POST requests"""
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        user = session.query(User).filter(User.email == data.get('email')).first()
        if user:
            raise HTTPConflict(description="Email already exists")
        if not 'address' in data:
            raise HTTPBadRequest(description={"address": "Address is required"})
        address = data.pop('address')
        schema = UserSchema()
        result = schema.load(data)
        if result.errors:
            raise HTTPBadRequest(description=result.errors)
        addressSchema = AddressSchema()
        addressResult = addressSchema.load(address)
        if addressResult.errors:
            raise HTTPBadRequest(description=addressResult.errors)
        user = User(**result.data)
        session.add(user)
        session.commit()
        address = Address(**addressResult.data)
        session.refresh(user)
        address.user = user.id
        session.add(address)
        session.commit()
        schema = UserSchema(exclude=('password',))
        result = schema.dump(user)
        resp.body = dumps({"user": result.data}, cls=DateTimeEncoder)


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
            "exp": datetime.utcnow() + REFRESH_TOKEN_EXPIRATION,
            "uid": user.id
        }
        token = encode(token_data, SECRET)
        refresh_token = encode(refresh_token_data, SECRET)
        resp.body = dumps({"token": token.decode("utf-8"), "refresh_token": refresh_token.decode("utf-8")})


class UserRefreshResource(object):
    def on_post(self, req, resp):
        """Handles POST requests"""
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        if not 'refresh_token' in data:
            raise HTTPBadRequest(description="Refresh token required")
        refresh_token = data['refresh_token']
        try:
            decoded = decode(refresh_token, SECRET, audience=TOKEN_AUDIENCE)
        except ExpiredSignatureError as e:
            raise HTTPBadRequest(description={"refresh_token": "Token has expired"})
        except DecodeError as e:
            raise HTTPBadRequest(description={"refresh_token": "Token could not be decoded"})
        else:
            new_token_data = decoded
            new_token_data['exp'] = datetime.utcnow() + TOKEN_EXPIRATION
            new_token = encode(new_token_data, SECRET)
            new_refresh_token_data = decoded
            new_refresh_token_data['exp'] = datetime.utcnow() + REFRESH_TOKEN_EXPIRATION
            new_refresh_token = encode(new_refresh_token_data, SECRET)
        resp.body = dumps({"token": new_token.decode("utf-8"), "refresh_token": new_refresh_token.decode("utf-8")})


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
        schema = UserSchema(exclude=('password',))
        resp.body = dumps({"user": schema.dump(user).data})


class UserUpdateResource(object):
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        user = session.query(User).get(req.uid)
        schema = UserSchema(exclude=('password', 'entity_type', 'date_of_birth'))
        result = schema.load(data)
        if result.errors:
            raise HTTPBadRequest(description=result.errors)
        session.query(User).filter(User.id == req.uid).update(result.data)
        session.commit()
        schema = UserSchema(exclude=('password',))
        result = schema.dump(user)
        resp.body = dumps({"user": result.data}, cls=DateTimeEncoder)


class UserAddressResource(object):
    @before(validate_token)
    def on_post(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        user = session.query(User).get(req.uid)
        schema = AddressSchema()
        result = schema.load(data)
        if result.errors:
            raise HTTPBadRequest(description=result.errors)
        address = Address(**result.data)
        address.user = req.uid
        session.add(address)
        session.commit()
        result = schema.dump(address)
        resp.body = dumps({"address": result.data}, cls=DateTimeEncoder)

    @before(validate_token)
    def on_put(self, req, resp):
        try:
            data = load(req.bounded_stream)
        except ValueError:
            raise HTTPBadRequest(description="Invalid request")
        user = session.query(User).get(req.uid)
        schema = AddressSchema()
        result = schema.load(data)
        if result.errors:
            raise HTTPBadRequest(description=result.errors)
        session.query(Address).filter(Address.id == user.address.id).update(result.data)
        session.commit()
        address = user.address
        result = schema.dump(address)
        resp.body = dumps({"address": result.data}, cls=DateTimeEncoder)
