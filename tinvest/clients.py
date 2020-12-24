# pylint:disable=too-many-lines
from http import HTTPStatus
from typing import Any, Optional, Type, TypeVar

from aiohttp import ClientSession
from pydantic import BaseModel
from requests import Session

from .apis import (
    accounts_get,
    market_bonds_get,
    market_candles_get,
    market_currencies_get,
    market_etfs_get,
    market_orderbook_get,
    market_search_by_figi_get,
    market_search_by_ticker_get,
    market_stocks_get,
    operations_get,
    orders_cancel_post,
    orders_get,
    orders_limit_order_post,
    orders_market_order_post,
    portfolio_currencies_get,
    portfolio_get,
    sandbox_clear_post,
    sandbox_currencies_balance_post,
    sandbox_positions_balance_post,
    sandbox_register_post,
    sandbox_remove_post,
)
from .constants import get_base_url
from .exceptions import BadRequestError, TooManyRequestsError, UnexpectedError
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
from .utils import set_default_headers, validate_token

__all__ = ('AsyncClient', 'SyncClient')

T = TypeVar('T', bound=BaseModel)  # pragma: no mutate


class AsyncClient:
    """
    ```python
    import os
    from tinvest import AsyncClient

    TOKEN = os.getenv('TINVEST_SANDBOX_TOKEN', '')

    async def main():
        client = AsyncClient(TOKEN, use_sandbox=True)
        ...
        await client.close()
    ```
    """

    def __init__(
        self,
        token: str,
        *,
        use_sandbox: bool = False,
        session: Optional[ClientSession] = None,
    ):
        validate_token(token)
        if not session:
            session = ClientSession()

        self._base_url = get_base_url(use_sandbox)
        self._token: str = token
        self._session = session

    async def __aenter__(self) -> 'AsyncClient':
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        await self.close()
        return exc_type is None

    async def _request(
        self, method: str, path: str, response_model: Type[T], **kwargs: Any
    ) -> T:
        url = self._base_url + path
        set_default_headers(kwargs, self._token)
        kwargs['raise_for_status'] = False

        async with self._session.request(method, url, **kwargs) as response:
            if response.status == HTTPStatus.OK:
                return response_model.parse_raw(await response.text())

            if response.status == HTTPStatus.BAD_REQUEST:
                raise BadRequestError(await response.text())

            if response.status == HTTPStatus.TOO_MANY_REQUESTS:
                raise TooManyRequestsError

            raise UnexpectedError(response.status, await response.text())

    async def close(self) -> None:
        await self._session.close()

    async def register_sandbox_account(
        self,
        body: SandboxRegisterRequest,
    ) -> SandboxRegisterResponse:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            body = SandboxRegisterRequest.tinkoff_iis()
            await client.register_sandbox_account(body)
        ```
        """
        return await sandbox_register_post(self._request, body)

    async def set_sandbox_currencies_balance(
        self,
        body: SandboxSetCurrencyBalanceRequest,
        broker_account_id: Optional[str] = None,
    ) -> Empty:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            body = SandboxSetCurrencyBalanceRequest(
                balance=1000,
                currency='RUB',
            )
            await client.set_sandbox_currencies_balance(body, broker_account_id)
        ```
        """
        return await sandbox_currencies_balance_post(
            self._request, body, broker_account_id
        )

    async def set_sandbox_positions_balance(
        self,
        body: SandboxSetPositionBalanceRequest,
        broker_account_id: Optional[str] = None,
    ) -> Empty:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            body = SandboxSetPositionBalanceRequest(
                balance=1000,
                figi='BBG0013HGFT4',
            )
            await client.set_sandbox_positions_balance(body, broker_account_id)
        ```
        """
        return await sandbox_positions_balance_post(
            self._request,
            body,
            broker_account_id,
        )

    async def remove_sandbox_account(
        self,
        broker_account_id: Optional[str] = None,
    ) -> Empty:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            await client.remove_sandbox_account(broker_account_id)
        ```
        """
        return await sandbox_remove_post(
            self._request,
            broker_account_id,
        )

    async def clear_sandbox_account(
        self,
        broker_account_id: Optional[str] = None,
    ) -> Empty:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            await client.clear_sandbox_account(broker_account_id)
        ```
        """
        return await sandbox_clear_post(
            self._request,
            broker_account_id,
        )

    async def get_orders(
        self,
        broker_account_id: Optional[str] = None,
    ) -> OrdersResponse:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            await client.get_orders(broker_account_id)
        ```
        """
        return await orders_get(
            self._request,
            broker_account_id,
        )

    async def post_orders_limit_order(
        self,
        figi: str,
        body: LimitOrderRequest,
        broker_account_id: Optional[str] = None,
    ) -> LimitOrderResponse:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            body = LimitOrderRequest(
                lots=2,
                operation='Buy',
                price=100.85,
            )
            await client.post_orders_limit_order(figi, body, broker_account_id)
        ```
        """
        return await orders_limit_order_post(
            self._request,
            figi,
            body,
            broker_account_id,
        )

    async def post_orders_market_order(
        self,
        figi: str,
        body: MarketOrderRequest,
        broker_account_id: Optional[str] = None,
    ) -> MarketOrderResponse:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            body = MarketOrderRequest(
                lots=2,
                operation='Buy'
            )
            await client.post_orders_market_order(figi, body, broker_account_id)
        ```
        """
        return await orders_market_order_post(
            self._request,
            figi,
            body,
            broker_account_id,
        )

    async def post_orders_cancel(
        self,
        order_id: str,
        broker_account_id: Optional[str] = None,
    ) -> Empty:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            await client.post_orders_cancel(order_id, broker_account_id)
        ```
        """
        return await orders_cancel_post(
            self._request,
            order_id,
            broker_account_id,
        )

    async def get_portfolio(
        self,
        broker_account_id: Optional[str] = None,
    ) -> PortfolioResponse:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            await client.get_portfolio(broker_account_id)
        ```
        """
        return await portfolio_get(
            self._request,
            broker_account_id,
        )

    async def get_portfolio_currencies(
        self,
        broker_account_id: Optional[str] = None,
    ) -> PortfolioCurrenciesResponse:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            await client.get_portfolio_currencies(broker_account_id)
        ```
        """
        return await portfolio_currencies_get(
            self._request,
            broker_account_id,
        )

    async def get_market_stocks(
        self,
    ) -> MarketInstrumentListResponse:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            await client.get_market_stocks()
        ```
        """
        return await market_stocks_get(
            self._request,
        )

    async def get_market_bonds(
        self,
    ) -> MarketInstrumentListResponse:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            await client.get_market_bonds()
        ```
        """
        return await market_bonds_get(
            self._request,
        )

    async def get_market_etfs(
        self,
    ) -> MarketInstrumentListResponse:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            await client.get_market_etfs()
        ```
        """
        return await market_etfs_get(
            self._request,
        )

    async def get_market_currencies(
        self,
    ) -> MarketInstrumentListResponse:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            await client.get_market_currencies()
        ```
        """
        return await market_currencies_get(
            self._request,
        )

    async def get_market_orderbook(
        self,
        figi: str,
        depth: int,
    ) -> OrderbookResponse:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            await client.get_market_orderbook(figi, depth)
        ```
        """
        return await market_orderbook_get(self._request, figi, depth)

    async def get_market_candles(
        self,
        figi: str,
        from_: datetime_or_str,
        to: datetime_or_str,
        interval: CandleResolution,
    ) -> CandlesResponse:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            await client.get_market_candles(figi, from_, to, interval)
        ```
        """
        return await market_candles_get(
            self._request,
            figi,
            from_,
            to,
            interval,
        )

    async def get_market_search_by_figi(
        self,
        figi: str,
    ) -> SearchMarketInstrumentResponse:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            await client.get_market_search_by_figi(figi)
        ```
        """
        return await market_search_by_figi_get(
            self._request,
            figi,
        )

    async def get_market_search_by_ticker(
        self,
        ticker: str,
    ) -> MarketInstrumentListResponse:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            await client.get_market_search_by_ticker(ticker)
        ```
        """
        return await market_search_by_ticker_get(
            self._request,
            ticker,
        )

    async def get_operations(
        self,
        from_: datetime_or_str,
        to: datetime_or_str,
        figi: Optional[str] = None,
        broker_account_id: Optional[str] = None,
    ) -> OperationsResponse:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            await client.get_operations(from_, to, figi, broker_account_id)
        ```
        """
        return await operations_get(
            self._request,
            from_,
            to,
            figi,
            broker_account_id,
        )

    async def get_accounts(
        self,
    ) -> UserAccountsResponse:
        """
        ```python
        async def main():
            client = AsyncClient(TOKEN, use_sandbox=True)
            await client.get_accounts()
        ```
        """
        return await accounts_get(
            self._request,
        )


class SyncClient:
    """
    ```python
    import os
    from tinvest import SyncClient

    TOKEN = os.getenv('TINVEST_SANDBOX_TOKEN', '')

    def main():
        client = SyncClient(TOKEN, use_sandbox=True)

        # SyncClient methods like AsyncClient methods
        market_bonds = client.get_market_bonds()
    ```
    """

    def __init__(
        self,
        token: str,
        *,
        use_sandbox: bool = False,
        session: Optional[Session] = None,
    ):
        validate_token(token)
        if not session:
            session = Session()

        self._base_url = get_base_url(use_sandbox)
        self._token: str = token
        self._session = session

    def _request(
        self,
        method: str,
        path: str,
        response_model: Type[T],
        **kwargs: Any,
    ) -> T:
        url = self._base_url + path
        set_default_headers(kwargs, self._token)

        response = self._session.request(method, url, **kwargs)
        if response.status_code == HTTPStatus.OK:
            return response_model.parse_raw(response.text)

        if response.status_code == HTTPStatus.BAD_REQUEST:
            raise BadRequestError(response.text)

        if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
            raise TooManyRequestsError

        raise UnexpectedError(response.status_code, response.text)

    def register_sandbox_account(
        self,
        body: SandboxRegisterRequest,
    ) -> SandboxRegisterResponse:
        return sandbox_register_post(self._request, body)

    def set_sandbox_currencies_balance(
        self,
        body: SandboxSetCurrencyBalanceRequest,
        broker_account_id: Optional[str] = None,
    ) -> Empty:
        return sandbox_currencies_balance_post(self._request, body, broker_account_id)

    def set_sandbox_positions_balance(
        self,
        body: SandboxSetPositionBalanceRequest,
        broker_account_id: Optional[str] = None,
    ) -> Empty:
        return sandbox_positions_balance_post(
            self._request,
            body,
            broker_account_id,
        )

    def remove_sandbox_account(
        self,
        broker_account_id: Optional[str] = None,
    ) -> Empty:
        return sandbox_remove_post(
            self._request,
            broker_account_id,
        )

    def clear_sandbox_account(
        self,
        broker_account_id: Optional[str] = None,
    ) -> Empty:
        return sandbox_clear_post(
            self._request,
            broker_account_id,
        )

    def get_orders(
        self,
        broker_account_id: Optional[str] = None,
    ) -> OrdersResponse:
        return orders_get(
            self._request,
            broker_account_id,
        )

    def post_orders_limit_order(
        self,
        figi: str,
        body: LimitOrderRequest,
        broker_account_id: Optional[str] = None,
    ) -> LimitOrderResponse:
        return orders_limit_order_post(
            self._request,
            figi,
            body,
            broker_account_id,
        )

    def post_orders_market_order(
        self,
        figi: str,
        body: MarketOrderRequest,
        broker_account_id: Optional[str] = None,
    ) -> MarketOrderResponse:
        return orders_market_order_post(
            self._request,
            figi,
            body,
            broker_account_id,
        )

    def post_orders_cancel(
        self,
        order_id: str,
        broker_account_id: Optional[str] = None,
    ) -> Empty:
        return orders_cancel_post(
            self._request,
            order_id,
            broker_account_id,
        )

    def get_portfolio(
        self,
        broker_account_id: Optional[str] = None,
    ) -> PortfolioResponse:
        return portfolio_get(
            self._request,
            broker_account_id,
        )

    def get_portfolio_currencies(
        self,
        broker_account_id: Optional[str] = None,
    ) -> PortfolioCurrenciesResponse:
        return portfolio_currencies_get(
            self._request,
            broker_account_id,
        )

    def get_market_stocks(
        self,
    ) -> MarketInstrumentListResponse:
        return market_stocks_get(
            self._request,
        )

    def get_market_bonds(
        self,
    ) -> MarketInstrumentListResponse:
        return market_bonds_get(
            self._request,
        )

    def get_market_etfs(
        self,
    ) -> MarketInstrumentListResponse:
        return market_etfs_get(
            self._request,
        )

    def get_market_currencies(
        self,
    ) -> MarketInstrumentListResponse:
        return market_currencies_get(
            self._request,
        )

    def get_market_orderbook(
        self,
        figi: str,
        depth: int,
    ) -> OrderbookResponse:
        return market_orderbook_get(self._request, figi, depth)

    def get_market_candles(
        self,
        figi: str,
        from_: datetime_or_str,
        to: datetime_or_str,
        interval: CandleResolution,
    ) -> CandlesResponse:
        return market_candles_get(
            self._request,
            figi,
            from_,
            to,
            interval,
        )

    def get_market_search_by_figi(
        self,
        figi: str,
    ) -> SearchMarketInstrumentResponse:
        return market_search_by_figi_get(
            self._request,
            figi,
        )

    def get_market_search_by_ticker(
        self,
        ticker: str,
    ) -> MarketInstrumentListResponse:
        return market_search_by_ticker_get(
            self._request,
            ticker,
        )

    def get_operations(
        self,
        from_: datetime_or_str,
        to: datetime_or_str,
        figi: Optional[str] = None,
        broker_account_id: Optional[str] = None,
    ) -> OperationsResponse:
        return operations_get(
            self._request,
            from_,
            to,
            figi,
            broker_account_id,
        )

    def get_accounts(
        self,
    ) -> UserAccountsResponse:
        return accounts_get(
            self._request,
        )
