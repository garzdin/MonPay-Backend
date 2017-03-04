from falcon import API
from falcon_cors import CORS
from controllers.file import *
from controllers.user import *
from controllers.beneficiary import *
from controllers.transaction import *
from controllers.account import *
from controllers.currency import *

__all__ = ['app']

cors = CORS(allow_all_origins=True)

app = API(middleware=[cors.middleware])
app.add_route('/api/v1/upload/file', FileUploadResource())
app.add_route('/api/v1/auth/create', UserCreateResource())
app.add_route('/api/v1/auth/login', UserLoginResource())
app.add_route('/api/v1/auth/refresh', UserRefreshResource())
app.add_route('/api/v1/auth/reset', UserResetResource())
app.add_route('/api/v1/user', UserGetResource())
app.add_route('/api/v1/user/update', UserUpdateResource())
app.add_route('/api/v1/user/address', UserAddressResource())
app.add_route('/api/v1/account', AccountListResource())
app.add_route('/api/v1/account/{id}', AccountGetResource())
app.add_route('/api/v1/account/{id}/activate', AccountUpdateStatusResource())
app.add_route('/api/v1/account/create', AccountCreateResource())
app.add_route('/api/v1/account/update', AccountUpdateResource())
app.add_route('/api/v1/account/delete', AccountDeleteResource())
app.add_route('/api/v1/currency', CurrencyListResource())
app.add_route('/api/v1/currency/{id}', CurrencyGetResource())
app.add_route('/api/v1/beneficiary', BeneficiaryListResource())
app.add_route('/api/v1/beneficiary/{id}', BeneficiaryGetResource())
app.add_route('/api/v1/beneficiary/create', BeneficiaryCreateResource())
app.add_route('/api/v1/beneficiary/update', BeneficiaryUpdateResource())
app.add_route('/api/v1/beneficiary/delete', BeneficiaryDeleteResource())
app.add_route('/api/v1/transaction', TransactionListResource())
app.add_route('/api/v1/transaction/{id}', TransactionGetResource())
app.add_route('/api/v1/transaction/create', TransactionCreateResource())
app.add_route('/api/v1/transaction/delete', TransactionDeleteResource())
