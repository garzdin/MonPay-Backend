import jwt
import falcon
from settings import SECRET, TOKEN_AUDIENCE

def validate_token(req, resp, resource, param):
    token = req.get_header('Authorization')
    if not token:
        raise falcon.HTTPBadRequest('Bad Request', 'Missing authorization token.')
    decoded = jwt.decode(token, SECRET, audience=TOKEN_AUDIENCE)
    req.uid = int(decoded['uid'])
