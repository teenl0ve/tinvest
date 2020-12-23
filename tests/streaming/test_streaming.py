import pytest

from tinvest import Streaming

pytestmark = pytest.mark.asyncio


async def test_closed_session(token, closed_session):
    async with Streaming(token, session=closed_session):
        pass
