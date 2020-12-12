# pylint:disable=redefined-outer-name
from datetime import datetime, timedelta

from tinvest import (
    CandleResolution,
    CandlesResponse,
    MarketInstrumentListResponse,
    OrderbookResponse,
    SearchMarketInstrumentResponse,
)
from tinvest.apis import (
    market_bonds_get,
    market_candles_get,
    market_currencies_get,
    market_etfs_get,
    market_orderbook_get,
    market_search_by_figi_get,
    market_search_by_ticker_get,
    market_stocks_get,
)


def test_market_stocks_get(http_request):
    market_stocks_get(
        http_request,
    )
    http_request.assert_called_once_with(
        'GET', '/market/stocks', response_model=MarketInstrumentListResponse
    )


def test_market_bonds_get(http_request):
    market_bonds_get(
        http_request,
    )
    http_request.assert_called_once_with(
        'GET',
        '/market/bonds',
        response_model=MarketInstrumentListResponse,
    )


def test_market_etfs_get(http_request):
    market_etfs_get(
        http_request,
    )
    http_request.assert_called_once_with(
        'GET',
        '/market/etfs',
        response_model=MarketInstrumentListResponse,
    )


def test_market_currencies_get(http_request):
    market_currencies_get(
        http_request,
    )
    http_request.assert_called_once_with(
        'GET',
        '/market/currencies',
        response_model=MarketInstrumentListResponse,
    )


def test_market_orderbook_get(http_request, figi):
    market_orderbook_get(http_request, figi, 2)
    http_request.assert_called_once_with(
        'GET',
        '/market/orderbook',
        response_model=OrderbookResponse,
        params={'figi': figi, 'depth': 2},
    )


def test_market_candles_get(http_request, figi):
    to = datetime.now()
    from_ = to - timedelta(days=7)
    market_candles_get(
        http_request, figi, from_.isoformat(), to.isoformat(), CandleResolution.min1
    )
    http_request.assert_called_once_with(
        'GET',
        '/market/candles',
        response_model=CandlesResponse,
        params={
            'figi': figi,
            'from': from_.isoformat(),
            'to': to.isoformat(),
            'interval': CandleResolution.min1,
        },
    )


def test_market_search_by_figi_get(http_request, figi):
    market_search_by_figi_get(http_request, figi)
    http_request.assert_called_once_with(
        'GET',
        '/market/search/by-figi',
        response_model=SearchMarketInstrumentResponse,
        params={'figi': figi},
    )


def test_market_search_by_ticker_get(http_request):
    ticker = 'some_ticker'
    market_search_by_ticker_get(http_request, ticker)
    http_request.assert_called_once_with(
        'GET',
        '/market/search/by-ticker',
        response_model=MarketInstrumentListResponse,
        params={'ticker': ticker},
    )
