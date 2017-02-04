from falcon import API
import currencycloud
from middleware.multipart import MultipartMiddleware
from controllers.misc import *
from controllers.user import *
from controllers.beneficiary import *
from controllers.conversion import *

__all__ = ['app']

currencycloud.environment = currencycloud.ENV_DEMOSTRATION
currencycloud.login_id = 'rjnienaber@gmail.com'
currencycloud.api_key = 'ef0fd50fca1fb14c1fab3a8436b9ecb65f02f129fd87eafa45ded8ae257528f0'

app = API(middleware=[MultipartMiddleware()])
app.add_route('/api/v1/upload/file', FileUploadResource())
app.add_route('/api/v1/user/create', UserCreateResource())
app.add_route('/api/v1/user/login', UserLoginResource())
app.add_route('/api/v1/user/reset', UserResetResource())
app.add_route('/api/v1/user/me', UserResource())
# app.add_route('/api/v1/user/me/update', UserUpdateResource())
app.add_route('/api/v1/beneficiary', BeneficiaryListResource())
app.add_route('/api/v1/beneficiary/{id}', BeneficiaryGetResource())
app.add_route('/api/v1/beneficiary/create', BeneficiaryCreateResource())
app.add_route('/api/v1/beneficiary/update', BeneficiaryUpdateResource())
app.add_route('/api/v1/beneficiary/delete', BeneficiaryDeleteResource())
app.add_route('/api/v1/beneficiary/required', BeneficiaryDetailsResource())
app.add_route('/api/v1/conversion', ConversionListResource())
app.add_route('/api/v1/conversion/{pair}', ConversionGetResource())
app.add_route('/api/v1/conversion/create', ConversionCreateResource())
app.add_route('/api/v1/conversion/dates', ConversionDatesResource())
# app.add_route('/api/v1/payment', PaymentFindResource())
# app.add_route('/api/v1/payment/:id', PaymentGetResource())
# app.add_route('/api/v1/payment/create', PaymentCreateResource())
# app.add_route('/api/v1/payment/:id/update', PaymentUpdateResource())
# app.add_route('/api/v1/payment/:id/delete', PaymentDeleteResource())
# app.add_route('/api/v1/payment/dates', PaymentDatesResource())
# app.add_route('/api/v1/currency', CurrencyListResource())
# app.add_route('/api/v1/currency/rate', CurrencyRateResource())
# app.add_route('/api/v1/transaction', TransactionListResource())
# app.add_route('/api/v1/transaction/:id', TransactionGetResource())
# app.add_route('/api/v1/ref/:id/delete', PaymentDeleteResource())
# app.add_route('/api/v1/analytics', AnalyticsResource())
