from falcon import API
from middleware.multipart import MultipartMiddleware
from controllers.user import *
from controllers.misc import *

__all__ = ['app']

app = API(middleware=[MultipartMiddleware()])
app.add_route('/api/v1/upload/file', FileUploadResource())
app.add_route('/api/v1/user/create', UserCreateResource())
app.add_route('/api/v1/user/login', UserLoginResource())
app.add_route('/api/v1/user/reset', UserResetResource())
app.add_route('/api/v1/user/me', UserResource())
