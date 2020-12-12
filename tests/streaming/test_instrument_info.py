# pylint:disable=redefined-outer-name
import json

import pytest

from tinvest import InstrumentInfoStreamingResponse, Streaming

pytestmark = pytest.mark.asyncio


@pytest.fixture()
def instrument_info_payload(figi):
    return {
        'event': 'instrument_info',
        'time': '2019-08-07T15:35:00.029721253Z',
        'payload': {
            'figi': figi,
            'trade_status': 'normal_trading',
            'min_price_increment': 0.0025,
            'lot': 1000,
        },
    }


@pytest.fixture()
def instrument_info(instrument_info_payload):
    return InstrumentInfoStreamingResponse.parse_obj(instrument_info_payload)


@pytest.fixture()
async def _instrument_info_message(message, instrument_info_payload):
    message.data = json.dumps(instrument_info_payload)


@pytest.mark.usefixtures('_instrument_info_message')
async def test_streaming_instrument_info(streaming: Streaming, queue, instrument_info):
    async with streaming:
        assert (await queue.get()) == instrument_info
