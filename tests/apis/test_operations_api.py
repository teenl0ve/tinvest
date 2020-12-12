# pylint:disable=redefined-outer-name
from datetime import datetime, timedelta

from tinvest import OperationsResponse
from tinvest.apis import operations_get


def test_operations_get(http_request, figi, broker_account_id):
    to = datetime.now()
    from_ = to - timedelta(days=7)
    operations_get(
        http_request, from_.isoformat(), to.isoformat(), figi, broker_account_id
    )
    http_request.assert_called_once_with(
        'GET',
        '/operations',
        response_model=OperationsResponse,
        params={
            'figi': figi,
            'brokerAccountId': broker_account_id,
            'from': from_.isoformat(),
            'to': to.isoformat(),
        },
    )


def test_operations_get_without_optional_args(http_request):
    to = datetime.now()
    from_ = to - timedelta(days=7)
    operations_get(http_request, from_.isoformat(), to.isoformat())
    http_request.assert_called_once_with(
        'GET',
        '/operations',
        response_model=OperationsResponse,
        params={'from': from_.isoformat(), 'to': to.isoformat()},
    )
