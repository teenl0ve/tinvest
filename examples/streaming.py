"""Streaming.

    python -m examples.streaming
"""
import asyncio

from pydantic import BaseSettings

import tinvest as ti


class Config(BaseSettings):
    TOKEN: str
    SANDBOX_TOKEN: str

    class Config:
        env_prefix = 'TINVEST_'


config = Config()


async def main() -> None:
    async with ti.Streaming(config.TOKEN) as streaming:
        await streaming.candle.subscribe('BBG0013HGFT4', ti.CandleResolution.min1)
        await streaming.orderbook.subscribe('BBG0013HGFT4', 5)
        await streaming.instrument_info.subscribe('BBG0013HGFT4')
        async for event in streaming:
            print(event)  # noqa:T001


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
