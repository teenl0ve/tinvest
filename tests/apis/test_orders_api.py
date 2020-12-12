# pylint:disable=redefined-outer-name

from tinvest import (
    Empty,
    LimitOrderRequest,
    LimitOrderResponse,
    MarketOrderRequest,
    MarketOrderResponse,
    OperationType,
    OrdersResponse,
)
from tinvest.apis import (
    orders_cancel_post,
    orders_get,
    orders_limit_order_post,
    orders_market_order_post,
)


def test_orders_get(http_request, broker_account_id):
    orders_get(http_request, broker_account_id)
    http_request.assert_called_once_with(
        'GET',
        '/orders',
        response_model=OrdersResponse,
        params={'brokerAccountId': broker_account_id},
    )


def test_orders_get_without_broker_account_id(http_request):
    orders_get(
        http_request,
    )
    http_request.assert_called_once_with(
        'GET',
        '/orders',
        response_model=OrdersResponse,
        params={},
    )


def test_orders_limit_order_post(http_request, figi, broker_account_id):
    body = LimitOrderRequest(lots=3, operation=OperationType.buy, price=13.5)
    orders_limit_order_post(http_request, figi, body, broker_account_id)
    http_request.assert_called_once_with(
        'POST',
        '/orders/limit-order',
        response_model=LimitOrderResponse,
        params={'figi': figi, 'brokerAccountId': broker_account_id},
        data=body.json(by_alias=True),
    )


def test_orders_limit_order_post_without_broker_account_id(http_request, figi):
    body = LimitOrderRequest(lots=3, operation=OperationType.buy, price=13.5)
    orders_limit_order_post(http_request, figi, body)
    http_request.assert_called_once_with(
        'POST',
        '/orders/limit-order',
        response_model=LimitOrderResponse,
        params={'figi': figi},
        data=body.json(by_alias=True),
    )


def test_orders_market_order_post(http_request, figi, broker_account_id):
    body = MarketOrderRequest(lots=1, operation=OperationType.buy)
    orders_market_order_post(http_request, figi, body, broker_account_id)
    http_request.assert_called_once_with(
        'POST',
        '/orders/market-order',
        response_model=MarketOrderResponse,
        params={'figi': figi, 'brokerAccountId': broker_account_id},
        data=body.json(by_alias=True),
    )


def test_orders_market_order_post_without_broker_account_id(http_request, figi):
    body = MarketOrderRequest(lots=1, operation=OperationType.buy)
    orders_market_order_post(http_request, figi, body)
    http_request.assert_called_once_with(
        'POST',
        '/orders/market-order',
        response_model=MarketOrderResponse,
        params={'figi': figi},
        data=body.json(by_alias=True),
    )


def test_orders_cancel_post(http_request, broker_account_id):
    order_id = 'some_order_id'
    orders_cancel_post(http_request, order_id, broker_account_id)
    http_request.assert_called_once_with(
        'POST',
        '/orders/cancel',
        response_model=Empty,
        params={'orderId': order_id, 'brokerAccountId': broker_account_id},
    )


def test_orders_cancel_post_without_broker_account_id(http_request):
    order_id = 'some_order_id'
    orders_cancel_post(http_request, order_id)
    http_request.assert_called_once_with(
        'POST',
        '/orders/cancel',
        response_model=Empty,
        params={'orderId': order_id},
    )
