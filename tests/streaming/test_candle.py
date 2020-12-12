# pylint:disable=redefined-outer-name
import json

import pytest

from tinvest import CandleStreamingResponse, Streaming

pytestmark = pytest.mark.asyncio


@pytest.fixture()
def candle_payload(figi):
    return {
        'event': 'candle',
        'time': '2019-08-07T15:35:00.029721253Z',
        'payload': {
            'o': 64.0575,
            'c': 64.0575,
            'h': 64.0575,
            'l': 64.0575,
            'v': 156,
            'time': '2019-08-07T15:35:00Z',
            'interval': '5min',
            'figi': figi,
        },
    }


@pytest.fixture()
def candle(candle_payload):
    return CandleStreamingResponse.parse_obj(candle_payload)


@pytest.fixture()
async def _candle_message(message, candle_payload):
    message.data = json.dumps(candle_payload)


@pytest.mark.usefixtures('_candle_message')
async def test_streaming_candle(streaming: Streaming, queue, candle):
    async with streaming:
        assert (await queue.get()) == candle
