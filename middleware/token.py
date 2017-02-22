from json import dumps
from jwt import decode, ExpiredSignatureError, DecodeError
from falcon import HTTPBadRequest, HTTPNotFound
from settings import SECRET, TOKEN_AUDIENCE
from models.models import User, session

__all__ = ['validate_token']


def validate_token(req, resp, resource, param):
    token = req.get_header('Authorization')
    if not token:
        raise HTTPBadRequest('Bad Request', 'Missing authorization token')
    try:
        decoded = decode(token, SECRET, audience=TOKEN_AUDIENCE)
    except ExpiredSignatureError as e:
        raise HTTPBadRequest(description={"token": "Token has expired"})
    except DecodeError as e:
        raise HTTPBadRequest(description={"token": "Token could not be decoded"})
    else:
        user = session.query(User).get(decoded.get('uid'))
        if not user:
            raise HTTPNotFound(description="User not found")
        req.uid = int(decoded.get('uid'))
