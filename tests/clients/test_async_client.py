# pylint:disable=redefined-outer-name
# pylint:disable=protected-access
import aiohttp
import pytest

from tinvest import AsyncClient, Empty
from tinvest.constants import PRODUCTION
from tinvest.exceptions import BadRequestError, TooManyRequestsError, UnexpectedError

pytestmark = pytest.mark.asyncio


@pytest.fixture()
def async_client(mocker):
    return mocker.AsyncMock()


@pytest.fixture()
def session(mocker, response):
    s = mocker.MagicMock()
    s.request.return_value.__aenter__.return_value = response
    s.close = mocker.AsyncMock()
    return s


@pytest.fixture()
def response(mocker, empty_raw):
    r = mocker.AsyncMock()
    r.status = 200
    r.text.return_value = empty_raw
    return r


@pytest.fixture()
def _too_many_requests(response):
    response.status = 429
    response.text.return_value = ''


@pytest.fixture()
def _unexpected_error(response):
    response.status = 500
    response.text.return_value = 'error'


@pytest.fixture()
def _bad_request(response, error_raw):
    response.status = 400
    response.text.return_value = error_raw


@pytest.fixture()
def async_method(mocker, func):
    method_name, target_func, args = func

    target = mocker.patch(
        f'tinvest.clients.{target_func}', autospec=True, side_effect=mocker.AsyncMock()
    )
    method = getattr(AsyncClient, method_name)

    return method, target, args


async def test_async_client(async_client, async_method):
    method, target, args = async_method

    await method(async_client, *args)
    # pylint:disable=protected-access
    target.assert_called_once_with(async_client._request, *args)


async def test_default_session(token):
    client = AsyncClient(token)

    assert isinstance(client._session, aiohttp.ClientSession)


async def test_request(token, session, tracking_id, headers):
    client = AsyncClient(token, session=session)

    result = await client._request('GET', '/path', Empty, params={'k': 1})

    assert result.tracking_id == tracking_id
    session.request.assert_called_once_with(
        'GET',
        f'{PRODUCTION}/path',
        headers=headers,
        params={'k': 1},
        raise_for_status=False,
    )


async def test_request_with_ctx(token, session, tracking_id, headers):
    async with AsyncClient(token, session=session) as client:
        result = await client._request('GET', '/path', Empty, params={'k': 1})

    assert result.tracking_id == tracking_id
    session.request.assert_called_once_with(
        'GET',
        f'{PRODUCTION}/path',
        headers=headers,
        params={'k': 1},
        raise_for_status=False,
    )
    session.close.assert_called_once_with()


@pytest.mark.usefixtures('_too_many_requests')
async def test_request_too_many_requests(token, session):
    client = AsyncClient(token, session=session)

    with pytest.raises(TooManyRequestsError):
        await client._request('GET', '/path', Empty)


@pytest.mark.usefixtures('_unexpected_error')
async def test_request_unexpected_error(token, session):
    client = AsyncClient(token, session=session)

    with pytest.raises(UnexpectedError):
        await client._request('GET', '/path', Empty)


@pytest.mark.usefixtures('_bad_request')
async def test_request_bad_request(token, session):
    client = AsyncClient(token, session=session)

    with pytest.raises(BadRequestError):
        await client._request('GET', '/path', Empty)
