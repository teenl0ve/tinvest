# pylint:disable=redefined-outer-name
# pylint:disable=protected-access

import pytest
from aiohttp import ClientSession, ClientWebSocketResponse, WSMessage, WSMsgType

from tinvest import Streaming


@pytest.fixture()
async def queue(streaming):
    return streaming._queue


@pytest.fixture()
async def message(mocker):
    msg = mocker.AsyncMock(WSMessage)
    msg.type = WSMsgType.TEXT
    return msg


@pytest.fixture()
async def ws(mocker):
    return mocker.AsyncMock(ClientWebSocketResponse)


@pytest.fixture()
async def session(mocker, ws, message):
    ws.__aiter__.return_value = [message]

    s = mocker.AsyncMock(ClientSession)
    s.closed = False
    s.ws_connect.return_value.__aenter__.return_value = ws
    s.ws_connect.return_value.__aexit__.return_value = False
    return s


@pytest.fixture()
def closed_session(session):
    session.closed = True
    return session


@pytest.fixture()
async def streaming(token, session):
    return Streaming(token, session=session, reconnect_enabled=False)
