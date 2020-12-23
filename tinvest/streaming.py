import asyncio
import logging
from typing import TYPE_CHECKING, Any, Optional, Set, TypeVar, Union

import aiohttp

from .constants import STREAMING
from .schemas import (
    CandleResolution,
    CandleStreamingResponse,
    CandleSubscription,
    ErrorStreamingResponse,
    Event,
    HashableModel,
    InstrumentInfoStreamingResponse,
    InstrumentInfoSubscription,
    OrderbookStreamingResponse,
    OrderbookSubscription,
    StreamingResponse,
)
from .utils import validate_token

__all__ = ('Streaming', 'CandleAPI', 'InstrumentInfoAPI', 'OrderbookAPI')

logger = logging.getLogger(__name__)

T = TypeVar('T')


class StopQueueType:
    def __repr__(self):
        return 'StopQueueType'

    def __copy__(self: T) -> T:
        return self

    def __deepcopy__(self: T, _: Any) -> T:
        return self


STOP_QUEUE = StopQueueType()

if TYPE_CHECKING:
    # pylint:disable=unsubscriptable-object
    _BaseQueue = asyncio.Queue[
        Union[
            CandleStreamingResponse,
            OrderbookStreamingResponse,
            InstrumentInfoStreamingResponse,
            ErrorStreamingResponse,
            StopQueueType,
        ]
    ]
else:
    _BaseQueue = asyncio.Queue


class _ClosedSessionError(Exception):
    pass


class Streaming:  # pylint:disable=too-many-instance-attributes
    """
    ```python
    from tinvest import CandleResolution, Streaming

    async def main():
        async with Streaming(TOKEN) as streaming:
            await streaming.candle.subscribe('BBG0013HGFT4', CandleResolution.min1)
            await streaming.orderbook.subscribe('BBG0013HGFT4', 5)
            await streaming.instrument_info.subscribe('BBG0013HGFT4')

            async for event in streaming:
                print(event)
                # responses
                # tinvest.InstrumentInfoStreamingResponse
                # tinvest.OrderbookStreamingResponse
                # tinvest.CandleStreamingResponse
                # tinvest.ErrorStreamingResponse

    ```
    """

    def __init__(
        self,
        token: str,
        *,
        session: Optional[aiohttp.ClientSession] = None,
        reconnect_enabled: bool = True,
        reconnect_timeout: float = 3,
        ws_close_timeout: float = 0,
        receive_timeout: Optional[float] = 5,
        heartbeat: Optional[float] = 3,
    ) -> None:
        validate_token(token)
        self._api: str = STREAMING
        self._token: str = token
        self._session: aiohttp.ClientSession = session or aiohttp.ClientSession()
        self._reconnect_enabled = reconnect_enabled
        self._reconnect_timeout = reconnect_timeout
        self._ws_close_timeout = ws_close_timeout
        self._receive_timeout = receive_timeout
        self._heartbeat = heartbeat

        self._queue: _BaseQueue = asyncio.Queue()
        self._ready = asyncio.Event()
        self._closing = asyncio.Event()
        self._ws_is_closed = asyncio.Event()
        self._lock = asyncio.Lock()
        self._connection_task: Optional[asyncio.Task] = None
        self.candle = CandleAPI()
        self.instrument_info = InstrumentInfoAPI()
        self.orderbook = OrderbookAPI()

    async def __aenter__(self) -> 'Streaming':
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> bool:
        await self.stop()
        return exc_type is None

    async def __aiter__(self):
        try:  # pylint:disable=too-many-nested-blocks
            while True:
                event = await self._queue.get()
                if event is STOP_QUEUE:
                    break
                yield event
        finally:
            await self._unsubscribe()

    async def start(self):
        self._connection_task = asyncio.create_task(self._run())
        await self._ready.wait()

    async def stop(self):
        await self._unsubscribe()
        await self._queue.put(STOP_QUEUE)
        self._closing.set()
        await self._ws_is_closed.wait()
        await self._session.close()
        if self._connection_task:
            await self._connection_task

    async def _run(self) -> None:
        if not self._reconnect_enabled:
            await self._connect()
            return

        while True:
            try:
                await self._connect()
            except _ClosedSessionError:
                break

    async def _connect(self) -> None:
        logger.info('Connecting to WebSocket')
        self._closing.clear()
        close_ws_task = None
        if self._session.closed:
            self._ready.set()
            self._ws_is_closed.set()
            raise _ClosedSessionError
        try:

            async with self._session.ws_connect(
                self._api,
                headers={'Authorization': f'Bearer {self._token}'},
                heartbeat=self._heartbeat,
                timeout=self._ws_close_timeout,
                receive_timeout=self._receive_timeout,
            ) as ws:
                logger.info('Connection established')
                self._ws_is_closed.clear()
                close_ws_task = asyncio.create_task(self._close_ws(ws))
                await self._handle_ws(ws)
        except asyncio.TimeoutError:
            logger.error('Timeout error. Try to reconnect')
            await asyncio.sleep(self._reconnect_timeout)
        except aiohttp.ClientConnectorError as e:
            logger.error('Connection error: %s. Try to reconnect', e)
            await asyncio.sleep(self._reconnect_timeout)
        finally:
            self._closing.set()
            if close_ws_task:
                await close_ws_task
                self._ready.clear()

    async def _close_ws(self, ws: aiohttp.ClientWebSocketResponse):
        try:
            await self._ready.wait()
            await self._closing.wait()
            await ws.close()
        finally:
            self._ws_is_closed.set()

    async def _handle_ws(self, ws: aiohttp.ClientWebSocketResponse):
        self.candle._set_ws(ws)  # pylint:disable=protected-access
        self.instrument_info._set_ws(ws)  # pylint:disable=protected-access
        self.orderbook._set_ws(ws)  # pylint:disable=protected-access
        await self._subscribe()
        self._ready.set()

        msg: aiohttp.WSMessage
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                response = StreamingResponse.parse_raw(msg.data)
                data = _parse_response(response)

                await self._queue.put(data)

            elif msg.type == aiohttp.WSMsgType.CLOSED:
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break

    async def _subscribe(self) -> None:
        # pylint:disable=protected-access
        await self.candle._subscribe_all()
        await self.instrument_info._subscribe_all()
        await self.orderbook._subscribe_all()

    async def _unsubscribe(self) -> None:
        # pylint:disable=protected-access
        await self.candle._unsubscribe_all()
        await self.instrument_info._unsubscribe_all()
        await self.orderbook._unsubscribe_all()


def _parse_response(response: StreamingResponse) -> Any:
    data: Any = None

    if response.event == Event.instrument_info:
        data = InstrumentInfoStreamingResponse.parse_obj(response.dict())

    if response.event == Event.orderbook:
        data = OrderbookStreamingResponse.parse_obj(response.dict())

    if response.event == Event.candle:
        data = CandleStreamingResponse.parse_obj(response.dict())

    if response.event == Event.error:
        data = ErrorStreamingResponse.parse_obj(response.dict())
        logger.error('Error response: %s', data)

    return data


class _BaseEventAPI:
    _event_name: Event

    def __init__(self):
        self._ws: Optional[aiohttp.ClientWebSocketResponse] = None
        self._subscriptions: Set[HashableModel] = set()

    @property
    def _subscription(self) -> str:
        return f'{self._event_name.value}:subscribe'

    @property
    def _unsubscription(self) -> str:
        return f'{self._event_name.value}:unsubscribe'

    def _set_ws(self, ws: aiohttp.ClientWebSocketResponse) -> None:
        self._ws = ws

    async def _subscribe_all(self) -> None:
        for payload in list(self._subscriptions):
            await self._send(payload, True)

    async def _unsubscribe_all(self) -> None:
        for payload in list(self._subscriptions):
            await self._send(payload)

    async def _send(
        self, payload: HashableModel, is_subscription: bool = False
    ) -> bool:
        if not self._ws or self._ws.closed:
            return False

        event: str
        if is_subscription:
            self._subscriptions.add(payload)
            event = self._subscription
        else:
            self._subscriptions.remove(payload)
            event = self._unsubscription

        await self._ws.send_json({'event': event, **payload.dict()})
        return True


class CandleAPI(_BaseEventAPI):
    _event_name = Event.candle

    def subscribe(
        self,
        figi: str,
        interval: CandleResolution,
        request_id: Optional[str] = None,
    ):
        return self._send(self._get_payload(figi, interval, request_id), True)

    def unsubscribe(
        self,
        figi: str,
        interval: CandleResolution,
        request_id: Optional[str] = None,
    ):
        return self._send(self._get_payload(figi, interval, request_id))

    def _get_payload(
        self,
        figi: str,
        interval: CandleResolution,
        request_id: Optional[str] = None,
    ) -> CandleSubscription:
        return CandleSubscription(
            figi=figi,
            interval=interval,
            request_id=request_id,
        )


class OrderbookAPI(_BaseEventAPI):
    _event_name = Event.orderbook

    def subscribe(self, figi: str, depth: int, request_id: Optional[str] = None):
        return self._send(self._get_payload(figi, depth, request_id), True)

    def unsubscribe(self, figi: str, depth: int, request_id: Optional[str] = None):
        return self._send(self._get_payload(figi, depth, request_id))

    @staticmethod
    def _get_payload(
        figi: str, depth: int, request_id: Optional[str] = None
    ) -> OrderbookSubscription:
        return OrderbookSubscription(
            figi=figi,
            depth=depth,
            request_id=request_id,
        )


class InstrumentInfoAPI(_BaseEventAPI):
    _event_name = Event.instrument_info

    def subscribe(self, figi: str, request_id: Optional[str] = None):
        return self._send(self._get_payload(figi, request_id), True)

    def unsubscribe(self, figi: str, request_id: Optional[str] = None):
        return self._send(self._get_payload(figi, request_id))

    @staticmethod
    def _get_payload(
        figi: str, request_id: Optional[str] = None
    ) -> InstrumentInfoSubscription:
        return InstrumentInfoSubscription(figi=figi, request_id=request_id)
