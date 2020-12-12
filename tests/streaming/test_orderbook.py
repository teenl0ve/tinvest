# pylint:disable=redefined-outer-name
import json

import pytest

from tinvest import OrderbookStreamingResponse, Streaming

pytestmark = pytest.mark.asyncio


@pytest.fixture()
def orderbook_payload(figi):
    return {
        'event': 'orderbook',
        'time': '2019-08-07T15:35:00.029721253Z',
        'payload': {
            'figi': figi,
            'depth': 2,
            'bids': [[64.3525, 204], [64.1975, 276]],
            'asks': [[64.38, 227], [64.5225, 120]],
        },
    }


@pytest.fixture()
def orderbook(orderbook_payload):
    return OrderbookStreamingResponse.parse_obj(orderbook_payload)


@pytest.fixture()
async def _orderbook_message(message, orderbook_payload):
    message.data = json.dumps(orderbook_payload)


@pytest.mark.usefixtures('_orderbook_message')
async def test_streaming_orderbook(streaming: Streaming, queue, orderbook):
    async with streaming:
        assert (await queue.get()) == orderbook
