# pylint:disable=too-many-lines
from typing import Any, Awaitable, Callable, Optional, TypeVar, Union

from pydantic import BaseModel

from .schemas import (
    CandleResolution,
    CandlesResponse,
    Empty,
    LimitOrderRequest,
    LimitOrderResponse,
    MarketInstrumentListResponse,
    MarketOrderRequest,
    MarketOrderResponse,
    OperationsResponse,
    OrderbookResponse,
    OrdersResponse,
    PortfolioCurrenciesResponse,
    PortfolioResponse,
    SandboxRegisterRequest,
    SandboxRegisterResponse,
    SandboxSetCurrencyBalanceRequest,
    SandboxSetPositionBalanceRequest,
    SearchMarketInstrumentResponse,
    UserAccountsResponse,
)
from .typedefs import datetime_or_str
from .utils import isoformat

__all__ = (
    'accounts_get',
    'market_bonds_get',
    'market_candles_get',
    'market_currencies_get',
    'market_etfs_get',
    'market_orderbook_get',
    'market_search_by_figi_get',
    'market_search_by_ticker_get',
    'market_stocks_get',
    'operations_get',
    'orders_cancel_post',
    'orders_get',
    'orders_limit_order_post',
    'orders_market_order_post',
    'portfolio_currencies_get',
    'portfolio_get',
    'sandbox_clear_post',
    'sandbox_currencies_balance_post',
    'sandbox_positions_balance_post',
    'sandbox_register_post',
    'sandbox_remove_post',
)

T = TypeVar('T', bound=BaseModel)


SyncRequest = Callable[..., T]
AsyncRequest = Callable[..., Awaitable[T]]

Request = Union[SyncRequest[T], AsyncRequest[T]]
Response = Union[T, Awaitable[T]]


def sandbox_register_post(
    request: Request[SandboxRegisterResponse],
    body: SandboxRegisterRequest,
) -> Response[SandboxRegisterResponse]:
    """
    POST /sandbox/register
    """
    kwargs: Any = {}
    kwargs.setdefault('data', body.json(by_alias=True))
    return request(
        'POST',
        '/sandbox/register',
        response_model=SandboxRegisterResponse,
        **kwargs,
    )


def sandbox_currencies_balance_post(
    request: Request[Empty],
    body: SandboxSetCurrencyBalanceRequest,
    broker_account_id: Optional[str] = None,
) -> Response[Empty]:
    """
    POST /sandbox/currencies/balance
    """
    kwargs: Any = {}
    kwargs.setdefault('params', {})
    params = kwargs['params']
    if broker_account_id:
        params.setdefault('brokerAccountId', broker_account_id)
    kwargs.setdefault('data', body.json())
    return request(
        'POST',
        '/sandbox/currencies/balance',
        response_model=Empty,
        **kwargs,
    )


def sandbox_positions_balance_post(
    request: Request[Empty],
    body: SandboxSetPositionBalanceRequest,
    broker_account_id: Optional[str] = None,
) -> Response[Empty]:
    """
    POST /sandbox/positions/balance
    """
    kwargs: Any = {}
    kwargs.setdefault('params', {})
    params = kwargs['params']
    if broker_account_id:
        params.setdefault('brokerAccountId', broker_account_id)
    kwargs.setdefault('data', body.json())
    return request('POST', '/sandbox/positions/balance', response_model=Empty, **kwargs)


def sandbox_remove_post(
    request: Request[Empty],
    broker_account_id: Optional[str] = None,
) -> Response[Empty]:
    """POST /sandbox/remove"""
    kwargs: Any = {}
    kwargs.setdefault('params', {})
    params = kwargs['params']
    if broker_account_id:
        params.setdefault('brokerAccountId', broker_account_id)
    return request('POST', '/sandbox/remove', response_model=Empty, **kwargs)


def sandbox_clear_post(
    request: Request[Empty],
    broker_account_id: Optional[str] = None,
) -> Response[Empty]:
    """POST /sandbox/clear"""
    kwargs: Any = {}
    kwargs.setdefault('params', {})
    params = kwargs['params']
    if broker_account_id:
        params.setdefault('brokerAccountId', broker_account_id)
    return request('POST', '/sandbox/clear', response_model=Empty, **kwargs)


def orders_get(
    request: Request[OrdersResponse],
    broker_account_id: Optional[str] = None,
) -> Response[OrdersResponse]:
    """GET /orders"""
    kwargs: Any = {}
    kwargs.setdefault('params', {})
    params = kwargs['params']
    if broker_account_id:
        params.setdefault('brokerAccountId', broker_account_id)
    return request('GET', '/orders', response_model=OrdersResponse, **kwargs)


def orders_limit_order_post(
    request: Request[LimitOrderResponse],
    figi: str,
    body: LimitOrderRequest,
    broker_account_id: Optional[str] = None,
) -> Response[LimitOrderResponse]:
    """POST /orders/limit-order"""
    kwargs: Any = {}
    kwargs.setdefault('params', {})
    params = kwargs['params']
    params.setdefault('figi', figi)
    if broker_account_id:
        params.setdefault('brokerAccountId', broker_account_id)
    kwargs.setdefault('data', body.json())
    return request(
        'POST',
        '/orders/limit-order',
        response_model=LimitOrderResponse,
        **kwargs,
    )


def orders_market_order_post(
    request: Request[MarketOrderResponse],
    figi: str,
    body: MarketOrderRequest,
    broker_account_id: Optional[str] = None,
) -> Response[MarketOrderResponse]:
    """POST /orders/market-order"""
    kwargs: Any = {}
    kwargs.setdefault('params', {})
    params = kwargs['params']
    params.setdefault('figi', figi)
    if broker_account_id:
        params.setdefault('brokerAccountId', broker_account_id)
    kwargs.setdefault('data', body.json())
    return request(
        'POST', '/orders/market-order', response_model=MarketOrderResponse, **kwargs
    )


def orders_cancel_post(
    request: Request[Empty],
    order_id: str,
    broker_account_id: Optional[str] = None,
) -> Response[Empty]:
    """POST /orders/cancel"""
    kwargs: Any = {}
    kwargs.setdefault('params', {})
    params = kwargs['params']
    params.setdefault('orderId', order_id)
    if broker_account_id:
        params.setdefault('brokerAccountId', broker_account_id)
    return request('POST', '/orders/cancel', response_model=Empty, **kwargs)


def portfolio_get(
    request: Request[PortfolioResponse],
    broker_account_id: Optional[str] = None,
) -> Response[PortfolioResponse]:
    """GET /portfolio"""
    kwargs: Any = {}
    kwargs.setdefault('params', {})
    params = kwargs['params']
    if broker_account_id:
        params.setdefault('brokerAccountId', broker_account_id)
    return request('GET', '/portfolio', response_model=PortfolioResponse, **kwargs)


def portfolio_currencies_get(
    request: Request[PortfolioCurrenciesResponse],
    broker_account_id: Optional[str] = None,
) -> Response[PortfolioCurrenciesResponse]:
    """GET /portfolio/currencies"""
    kwargs: Any = {}
    kwargs.setdefault('params', {})
    params = kwargs['params']
    if broker_account_id:
        params.setdefault('brokerAccountId', broker_account_id)
    return request(
        'GET',
        '/portfolio/currencies',
        response_model=PortfolioCurrenciesResponse,
        **kwargs,
    )


def market_stocks_get(
    request: Request[MarketInstrumentListResponse],
) -> Response[MarketInstrumentListResponse]:
    """GET /market/stocks"""
    kwargs: Any = {}
    return request(
        'GET',
        '/market/stocks',
        response_model=MarketInstrumentListResponse,
        **kwargs,
    )


def market_bonds_get(
    request: Request[MarketInstrumentListResponse],
) -> Response[MarketInstrumentListResponse]:
    """GET /market/bonds"""
    kwargs: Any = {}
    return request(
        'GET',
        '/market/bonds',
        response_model=MarketInstrumentListResponse,
        **kwargs,
    )


def market_etfs_get(
    request: Request[MarketInstrumentListResponse],
) -> Response[MarketInstrumentListResponse]:
    """GET /market/etfs"""
    kwargs: Any = {}
    return request(
        'GET',
        '/market/etfs',
        response_model=MarketInstrumentListResponse,
        **kwargs,
    )


def market_currencies_get(
    request: Request[MarketInstrumentListResponse],
) -> Response[MarketInstrumentListResponse]:
    """GET /market/currencies"""
    kwargs: Any = {}
    return request(
        'GET',
        '/market/currencies',
        response_model=MarketInstrumentListResponse,
        **kwargs,
    )


def market_orderbook_get(
    request: Request[OrderbookResponse],
    figi: str,
    depth: int,
) -> Response[OrderbookResponse]:
    """GET /market/orderbook"""
    kwargs: Any = {}
    kwargs.setdefault('params', {})
    params = kwargs['params']
    params.setdefault('figi', figi)
    params.setdefault('depth', depth)
    return request(
        'GET',
        '/market/orderbook',
        response_model=OrderbookResponse,
        **kwargs,
    )


def market_candles_get(
    request: Request[CandlesResponse],
    figi: str,
    from_: datetime_or_str,
    to: datetime_or_str,
    interval: CandleResolution,
) -> Response[CandlesResponse]:
    """GET /market/candles"""
    kwargs: Any = {}
    kwargs.setdefault('params', {})
    params = kwargs['params']
    params.setdefault('figi', figi)
    params.setdefault('from', isoformat(from_))
    params.setdefault('to', isoformat(to))
    params.setdefault('interval', interval.value)
    return request('GET', '/market/candles', response_model=CandlesResponse, **kwargs)


def market_search_by_figi_get(
    request: Request[SearchMarketInstrumentResponse],
    figi: str,
) -> Response[SearchMarketInstrumentResponse]:
    """GET /market/search/by-figi"""
    kwargs: Any = {}
    kwargs.setdefault('params', {})
    params = kwargs['params']
    params.setdefault('figi', figi)
    return request(
        'GET',
        '/market/search/by-figi',
        response_model=SearchMarketInstrumentResponse,
        **kwargs,
    )


def market_search_by_ticker_get(
    request: Request[MarketInstrumentListResponse],
    ticker: str,
) -> Response[MarketInstrumentListResponse]:
    """GET /market/search/by-ticker"""
    kwargs: Any = {}
    kwargs.setdefault('params', {})
    params = kwargs['params']
    params.setdefault('ticker', ticker)
    return request(
        'GET',
        '/market/search/by-ticker',
        response_model=MarketInstrumentListResponse,
        **kwargs,
    )


def operations_get(
    request: Request[OperationsResponse],
    from_: datetime_or_str,
    to: datetime_or_str,
    figi: Optional[str] = None,
    broker_account_id: Optional[str] = None,
) -> Response[OperationsResponse]:
    """GET /operations"""
    kwargs: Any = {}
    kwargs.setdefault('params', {})
    params = kwargs['params']
    params.setdefault('from', isoformat(from_))
    params.setdefault('to', isoformat(to))
    if figi:
        params.setdefault('figi', figi)
    if broker_account_id:
        params.setdefault('brokerAccountId', broker_account_id)
    return request('GET', '/operations', response_model=OperationsResponse, **kwargs)


def accounts_get(
    request: Request[UserAccountsResponse],
) -> Response[UserAccountsResponse]:
    """GET /user/accounts"""
    kwargs: Any = {}
    return request(
        'GET', '/user/accounts', response_model=UserAccountsResponse, **kwargs
    )
