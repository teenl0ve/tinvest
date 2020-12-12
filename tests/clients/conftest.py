import json

import pytest

funcs = [
    ('get_accounts', 'accounts_get', 0),
    ('get_market_bonds', 'market_bonds_get', 0),
    ('get_market_candles', 'market_candles_get', 4),
    ('get_market_currencies', 'market_currencies_get', 0),
    ('get_market_etfs', 'market_etfs_get', 0),
    ('get_market_orderbook', 'market_orderbook_get', 2),
    ('get_market_search_by_figi', 'market_search_by_figi_get', 1),
    ('get_market_search_by_ticker', 'market_search_by_ticker_get', 1),
    ('get_market_stocks', 'market_stocks_get', 0),
    ('get_operations', 'operations_get', 4),
    ('post_orders_cancel', 'orders_cancel_post', 2),
    ('get_orders', 'orders_get', 1),
    ('post_orders_limit_order', 'orders_limit_order_post', 3),
    ('post_orders_market_order', 'orders_market_order_post', 3),
    ('get_portfolio_currencies', 'portfolio_currencies_get', 1),
    ('get_portfolio', 'portfolio_get', 1),
    ('clear_sandbox_account', 'sandbox_clear_post', 1),
    ('set_sandbox_currencies_balance', 'sandbox_currencies_balance_post', 2),
    ('set_sandbox_positions_balance', 'sandbox_positions_balance_post', 2),
    ('register_sandbox_account', 'sandbox_register_post', 1),
    ('remove_sandbox_account', 'sandbox_remove_post', 1),
]


@pytest.fixture(params=funcs)
def func(request):
    method_name, target_func, args_count = request.param
    args = list(range(args_count))

    return method_name, target_func, args


@pytest.fixture()
def empty_raw(tracking_id):
    return json.dumps(
        {
            'payload': {},
            'status': 'Ok',
            'trackingId': tracking_id,
        }
    )


@pytest.fixture()
def error_raw(tracking_id):
    return json.dumps(
        {
            'trackingId': tracking_id,
            'payload': {},
        }
    )
