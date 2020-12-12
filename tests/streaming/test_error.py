# pylint:disable=redefined-outer-name
import json

import pytest

from tinvest import ErrorStreamingResponse, Streaming

pytestmark = pytest.mark.asyncio


@pytest.fixture()
def error_payload(request_id):
    return {
        'event': 'error',
        'time': '2019-08-07T15:35:00.029721253Z',
        'payload': {
            'request_id': request_id,
            'error': 'Subscription instrument_info:subscribe. FIGI NOOOOOOO not found',
        },
    }


@pytest.fixture()
def error(error_payload):
    return ErrorStreamingResponse.parse_obj(error_payload)


@pytest.fixture()
async def _error_message(message, error_payload):
    message.data = json.dumps(error_payload)


@pytest.mark.usefixtures('_error_message')
async def test_streaming_error(streaming: Streaming, queue, error):
    async with streaming:
        assert (await queue.get()) == error
