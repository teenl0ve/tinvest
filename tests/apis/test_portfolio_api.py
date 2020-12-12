# pylint:disable=redefined-outer-name

from tinvest import PortfolioCurrenciesResponse, PortfolioResponse
from tinvest.apis import portfolio_currencies_get, portfolio_get


def test_portfolio_get(http_request, broker_account_id):
    portfolio_get(http_request, broker_account_id)
    http_request.assert_called_once_with(
        'GET',
        '/portfolio',
        response_model=PortfolioResponse,
        params={'brokerAccountId': broker_account_id},
    )


def test_portfolio_get_without_broker_account_id(http_request):
    portfolio_get(
        http_request,
    )
    http_request.assert_called_once_with(
        'GET',
        '/portfolio',
        response_model=PortfolioResponse,
        params={},
    )


def test_portfolio_currencies_get(http_request, broker_account_id):
    portfolio_currencies_get(http_request, broker_account_id)
    http_request.assert_called_once_with(
        'GET',
        '/portfolio/currencies',
        response_model=PortfolioCurrenciesResponse,
        params={'brokerAccountId': broker_account_id},
    )


def test_portfolio_currencies_get_without_broker_account_id(http_request):
    portfolio_currencies_get(
        http_request,
    )
    http_request.assert_called_once_with(
        'GET',
        '/portfolio/currencies',
        response_model=PortfolioCurrenciesResponse,
        params={},
    )
