"""Streaming.

    python -m examples.streaming_with_handlers
"""
import asyncio

from pydantic import BaseSettings

import tinvest


class Config(BaseSettings):
    TOKEN: str
    SANDBOX_TOKEN: str

    class Config:
        env_prefix = 'TINVEST_'


config = Config()


async def handle_reconnect():
    # No longer supported
    print('Reconnecting')  # noqa:T001


async def handle_candle(payload: tinvest.CandleStreaming):
    print(payload)  # noqa:T001


async def handle_orderbook(payload: tinvest.OrderbookStreaming):
    print(payload)  # noqa:T001


async def handle_instrument_info(payload: tinvest.InstrumentInfoStreaming):
    print(payload)  # noqa:T001


async def handle_error(payload: tinvest.ErrorStreaming):
    print(payload)  # noqa:T001


async def startup(streaming: tinvest.Streaming):
    await streaming.candle.subscribe('BBG0013HGFT4', tinvest.CandleResolution.min1)
    await streaming.orderbook.subscribe('BBG0013HGFT4', 5, '123ASD1123')
    await streaming.instrument_info.subscribe('BBG0013HGFT4')


HANDLER_BY_EVENT = {
    tinvest.Event.candle: handle_candle,
    tinvest.Event.orderbook: handle_orderbook,
    tinvest.Event.instrument_info: handle_instrument_info,
    tinvest.Event.error: handle_error,
}


async def main():
    async with tinvest.Streaming(config.TOKEN) as streaming:
        await startup(streaming)
        async for event in streaming:
            await HANDLER_BY_EVENT[event.event](event.payload)
        # Unsubscribed automatically


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
