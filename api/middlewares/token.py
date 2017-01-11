from json import dumps
from jwt import decode, ExpiredSignatureError, DecodeError
from falcon import HTTPBadRequest
from settings import SECRET, TOKEN_AUDIENCE

__all__ = ['validate_token']

def validate_token(req, resp, resource, param):
    token = req.get_header('Authorization')
    if not token:
        raise HTTPBadRequest('Bad Request', 'Missing authorization token.')
    try:
        decoded = decode(token, SECRET, audience=TOKEN_AUDIENCE)
    except ExpiredSignatureError as e:
        req.uid = None
        req.decode_error = str(e)
    except DecodeError as e:
        req.uid = None
        req.decode_error = str(e)
    else:
        req.uid = int(decoded['uid'])
