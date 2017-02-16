from json import dumps
from jwt import decode, ExpiredSignatureError, DecodeError
from falcon import HTTPBadRequest
from settings import SECRET, TOKEN_AUDIENCE

__all__ = ['validate_token']


def validate_token(req, resp, resource, param):
    token = req.get_header('Authorization')
    if not token:
        raise HTTPBadRequest('Bad Request', 'Missing authorization token')
    try:
        decoded = decode(token, SECRET, audience=TOKEN_AUDIENCE)
    except ExpiredSignatureError as e:
        raise HTTPBadRequest('Bad Request', 'Token has expired')
    except DecodeError as e:
        raise HTTPBadRequest('Bad Request', 'Token could not be decoded')
    else:
        req.uid = int(decoded['uid'])
