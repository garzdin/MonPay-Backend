from falcon import API
from middleware.multipart import MultipartMiddleware
from controllers.file import *
from controllers.user import *
from controllers.beneficiary import *

__all__ = ['app']

app = API(middleware=[MultipartMiddleware()])
app.add_route('/api/v1/upload/file', FileUploadResource())
app.add_route('/api/v1/auth/create', UserCreateResource())
app.add_route('/api/v1/auth/login', UserLoginResource())
app.add_route('/api/v1/auth/refresh', UserRefreshResource())
app.add_route('/api/v1/auth/reset', UserResetResource())
app.add_route('/api/v1/user', UserGetResource())
# app.add_route('/api/v1/user/me/update', UserUpdateResource())
app.add_route('/api/v1/beneficiary', BeneficiaryListResource())
app.add_route('/api/v1/beneficiary/{id}', BeneficiaryGetResource())
app.add_route('/api/v1/beneficiary/create', BeneficiaryCreateResource())
app.add_route('/api/v1/beneficiary/update', BeneficiaryUpdateResource())
app.add_route('/api/v1/beneficiary/delete', BeneficiaryDeleteResource())
# app.add_route('/api/v1/analytics', AnalyticsResource())
