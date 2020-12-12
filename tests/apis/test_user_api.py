# pylint:disable=redefined-outer-name

from tinvest import UserAccountsResponse
from tinvest.apis import accounts_get


def test_accounts_get(http_request):
    accounts_get(http_request)
    http_request.assert_called_once_with(
        'GET', '/user/accounts', response_model=UserAccountsResponse
    )
