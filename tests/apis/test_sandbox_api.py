# pylint:disable=redefined-outer-name

from tinvest import (
    BrokerAccountType,
    Empty,
    SandboxRegisterRequest,
    SandboxRegisterResponse,
    SandboxSetCurrencyBalanceRequest,
    SandboxSetPositionBalanceRequest,
)
from tinvest.apis import (
    sandbox_clear_post,
    sandbox_currencies_balance_post,
    sandbox_positions_balance_post,
    sandbox_register_post,
    sandbox_remove_post,
)


def test_sandbox_register(http_request):
    body = SandboxRegisterRequest(broker_account_type=BrokerAccountType.tinkoff)
    sandbox_register_post(http_request, body)
    http_request.assert_called_once_with(
        'POST',
        '/sandbox/register',
        response_model=SandboxRegisterResponse,
        data=body.json(by_alias=True),
    )


def test_sandbox_currencies_balance(http_request, broker_account_id):
    body = SandboxSetCurrencyBalanceRequest.parse_obj(
        {'balance': 1000.0, 'currency': 'USD'}
    )
    sandbox_currencies_balance_post(http_request, body, broker_account_id)
    http_request.assert_called_once_with(
        'POST',
        '/sandbox/currencies/balance',
        response_model=Empty,
        params={'brokerAccountId': broker_account_id},
        data=body.json(by_alias=True),
    )


def test_sandbox_currencies_balance_without_broker_account_id(http_request):
    body = SandboxSetCurrencyBalanceRequest.parse_obj(
        {'balance': 1000.0, 'currency': 'USD'}
    )
    sandbox_currencies_balance_post(http_request, body)
    http_request.assert_called_once_with(
        'POST',
        '/sandbox/currencies/balance',
        response_model=Empty,
        params={},
        data=body.json(by_alias=True),
    )


def test_sandbox_positions_balance(http_request, broker_account_id):
    body = SandboxSetPositionBalanceRequest.parse_obj(
        {'balance': 1000.0, 'figi': '<FIGI>'}
    )
    sandbox_positions_balance_post(http_request, body, broker_account_id)
    http_request.assert_called_once_with(
        'POST',
        '/sandbox/positions/balance',
        response_model=Empty,
        params={'brokerAccountId': broker_account_id},
        data=body.json(by_alias=True),
    )


def test_sandbox_positions_balance_without_broker_account_id(http_request):
    body = SandboxSetPositionBalanceRequest.parse_obj(
        {'balance': 1000.0, 'figi': '<FIGI>'}
    )
    sandbox_positions_balance_post(http_request, body)
    http_request.assert_called_once_with(
        'POST',
        '/sandbox/positions/balance',
        response_model=Empty,
        params={},
        data=body.json(by_alias=True),
    )


def test_sandbox_remove(http_request, broker_account_id):
    sandbox_remove_post(http_request, broker_account_id)
    http_request.assert_called_once_with(
        'POST',
        '/sandbox/remove',
        response_model=Empty,
        params={'brokerAccountId': broker_account_id},
    )


def test_sandbox_remove_without_broker_account_id(http_request):
    sandbox_remove_post(
        http_request,
    )
    http_request.assert_called_once_with(
        'POST',
        '/sandbox/remove',
        response_model=Empty,
        params={},
    )


def test_sandbox_clear(http_request, broker_account_id):
    sandbox_clear_post(http_request, broker_account_id)
    http_request.assert_called_once_with(
        'POST',
        '/sandbox/clear',
        response_model=Empty,
        params={'brokerAccountId': broker_account_id},
    )


def test_sandbox_clear_without_broker_account_id(http_request):
    sandbox_clear_post(
        http_request,
    )
    http_request.assert_called_once_with(
        'POST',
        '/sandbox/clear',
        response_model=Empty,
        params={},
    )
