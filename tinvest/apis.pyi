# pylint:disable=too-many-lines
from typing import Any, Awaitable, Callable, Optional, TypeVar, Union, overload

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
@overload
def sandbox_register_post(
    request: SyncRequest[SandboxRegisterResponse],
    body: SandboxRegisterRequest,
) -> SandboxRegisterResponse: ...
@overload
def sandbox_register_post(
    request: AsyncRequest[SandboxRegisterResponse],
    body: SandboxRegisterRequest,
) -> Awaitable[SandboxRegisterResponse]: ...
@overload
def sandbox_currencies_balance_post(
    request: SyncRequest[Empty],
    body: SandboxSetCurrencyBalanceRequest,
    broker_account_id: Optional[str] = None,
) -> Empty: ...
@overload
def sandbox_currencies_balance_post(
    request: AsyncRequest[Empty],
    body: SandboxSetCurrencyBalanceRequest,
    broker_account_id: Optional[str] = None,
) -> Awaitable[Empty]: ...
@overload
def sandbox_positions_balance_post(
    request: SyncRequest[Empty],
    body: SandboxSetPositionBalanceRequest,
    broker_account_id: Optional[str] = None,
) -> Empty: ...
@overload
def sandbox_positions_balance_post(
    request: AsyncRequest[Empty],
    body: SandboxSetPositionBalanceRequest,
    broker_account_id: Optional[str] = None,
) -> Awaitable[Empty]: ...
@overload
def sandbox_remove_post(
    request: SyncRequest[Empty],
    broker_account_id: Optional[str] = None,
) -> Empty: ...
@overload
def sandbox_remove_post(
    request: AsyncRequest[Empty],
    broker_account_id: Optional[str] = None,
) -> Awaitable[Empty]: ...
@overload
def sandbox_clear_post(
    request: SyncRequest[Empty],
    broker_account_id: Optional[str] = None,
) -> Empty: ...
@overload
def sandbox_clear_post(
    request: AsyncRequest[Empty],
    broker_account_id: Optional[str] = None,
) -> Awaitable[Empty]: ...
@overload
def orders_get(
    request: SyncRequest[OrdersResponse],
    broker_account_id: Optional[str] = None,
) -> OrdersResponse: ...
@overload
def orders_get(
    request: AsyncRequest[OrdersResponse],
    broker_account_id: Optional[str] = None,
) -> Awaitable[OrdersResponse]: ...
@overload
def orders_limit_order_post(
    request: SyncRequest[LimitOrderResponse],
    figi: str,
    body: LimitOrderRequest,
    broker_account_id: Optional[str] = None,
) -> LimitOrderResponse: ...
@overload
def orders_limit_order_post(
    request: AsyncRequest[LimitOrderResponse],
    figi: str,
    body: LimitOrderRequest,
    broker_account_id: Optional[str] = None,
) -> Awaitable[LimitOrderResponse]: ...
@overload
def orders_market_order_post(
    request: SyncRequest[MarketOrderResponse],
    figi: str,
    body: MarketOrderRequest,
    broker_account_id: Optional[str] = None,
) -> MarketOrderResponse: ...
@overload
def orders_market_order_post(
    request: AsyncRequest[MarketOrderResponse],
    figi: str,
    body: MarketOrderRequest,
    broker_account_id: Optional[str] = None,
) -> Awaitable[MarketOrderResponse]: ...
@overload
def orders_cancel_post(
    request: SyncRequest[Empty],
    order_id: str,
    broker_account_id: Optional[str] = None,
) -> Empty: ...
@overload
def orders_cancel_post(
    request: AsyncRequest[Empty],
    order_id: str,
    broker_account_id: Optional[str] = None,
) -> Awaitable[Empty]: ...
@overload
def portfolio_get(
    request: SyncRequest[PortfolioResponse],
    broker_account_id: Optional[str] = None,
) -> PortfolioResponse: ...
@overload
def portfolio_get(
    request: AsyncRequest[PortfolioResponse],
    broker_account_id: Optional[str] = None,
) -> Awaitable[PortfolioResponse]: ...
@overload
def portfolio_currencies_get(
    request: SyncRequest[PortfolioCurrenciesResponse],
    broker_account_id: Optional[str] = None,
) -> PortfolioCurrenciesResponse: ...
@overload
def portfolio_currencies_get(
    request: AsyncRequest[PortfolioCurrenciesResponse],
    broker_account_id: Optional[str] = None,
) -> Awaitable[PortfolioCurrenciesResponse]: ...
@overload
def market_stocks_get(
    request: SyncRequest[MarketInstrumentListResponse],
) -> MarketInstrumentListResponse: ...
@overload
def market_stocks_get(
    request: AsyncRequest[MarketInstrumentListResponse],
) -> Awaitable[MarketInstrumentListResponse]: ...
@overload
def market_bonds_get(
    request: SyncRequest[MarketInstrumentListResponse],
) -> MarketInstrumentListResponse: ...
@overload
def market_bonds_get(
    request: AsyncRequest[MarketInstrumentListResponse],
) -> Awaitable[MarketInstrumentListResponse]: ...
@overload
def market_etfs_get(
    request: SyncRequest[MarketInstrumentListResponse],
) -> MarketInstrumentListResponse: ...
@overload
def market_etfs_get(
    request: AsyncRequest[MarketInstrumentListResponse],
) -> Awaitable[MarketInstrumentListResponse]: ...
@overload
def market_currencies_get(
    request: SyncRequest[MarketInstrumentListResponse],
) -> MarketInstrumentListResponse: ...
@overload
def market_currencies_get(
    request: AsyncRequest[MarketInstrumentListResponse],
) -> Awaitable[MarketInstrumentListResponse]: ...
@overload
def market_orderbook_get(
    request: SyncRequest[OrderbookResponse],
    figi: str,
    depth: int,
) -> OrderbookResponse: ...
@overload
def market_orderbook_get(
    request: AsyncRequest[OrderbookResponse],
    figi: str,
    depth: int,
) -> Awaitable[OrderbookResponse]: ...
@overload
def market_candles_get(
    request: SyncRequest[CandlesResponse],
    figi: str,
    from_: datetime_or_str,
    to: datetime_or_str,
    interval: CandleResolution,
) -> CandlesResponse: ...
@overload
def market_candles_get(
    request: AsyncRequest[CandlesResponse],
    figi: str,
    from_: datetime_or_str,
    to: datetime_or_str,
    interval: CandleResolution,
) -> Awaitable[CandlesResponse]: ...
@overload
def market_search_by_figi_get(
    request: SyncRequest[SearchMarketInstrumentResponse],
    figi: str,
) -> SearchMarketInstrumentResponse: ...
@overload
def market_search_by_figi_get(
    request: AsyncRequest[SearchMarketInstrumentResponse],
    figi: str,
) -> Awaitable[SearchMarketInstrumentResponse]: ...
@overload
def market_search_by_ticker_get(
    request: SyncRequest[MarketInstrumentListResponse],
    ticker: str,
) -> MarketInstrumentListResponse: ...
@overload
def market_search_by_ticker_get(
    request: AsyncRequest[MarketInstrumentListResponse],
    ticker: str,
) -> Awaitable[MarketInstrumentListResponse]: ...
@overload
def operations_get(
    request: SyncRequest[OperationsResponse],
    from_: datetime_or_str,
    to: datetime_or_str,
    figi: Optional[str] = None,
    broker_account_id: Optional[str] = None,
) -> OperationsResponse: ...
@overload
def operations_get(
    request: AsyncRequest[OperationsResponse],
    from_: datetime_or_str,
    to: datetime_or_str,
    figi: Optional[str] = None,
    broker_account_id: Optional[str] = None,
) -> Awaitable[OperationsResponse]: ...
@overload
def accounts_get(
    request: SyncRequest[UserAccountsResponse],
) -> UserAccountsResponse: ...
@overload
def accounts_get(
    request: AsyncRequest[UserAccountsResponse],
) -> Awaitable[UserAccountsResponse]: ...
