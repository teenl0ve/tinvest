# pylint:disable=redefined-outer-name
# pylint:disable=protected-access
import pytest
import requests

from tinvest import Empty, SyncClient
from tinvest.constants import PRODUCTION
from tinvest.exceptions import BadRequestError, TooManyRequestsError, UnexpectedError


@pytest.fixture()
def sync_client(mocker):
    return mocker.Mock()


@pytest.fixture()
def session(mocker, response):
    s = mocker.Mock()
    s.request.return_value = response
    return s


@pytest.fixture()
def response(mocker, empty_raw):
    r = mocker.Mock()
    r.status_code = 200
    r.text = empty_raw
    return r


@pytest.fixture()
def _too_many_requests(response):
    response.status_code = 429
    response.text = ''


@pytest.fixture()
def _unexpected_error(response):
    response.status_code = 500
    response.text = 'error'


@pytest.fixture()
def _bad_request(response, error_raw):
    response.status_code = 400
    response.text = error_raw


@pytest.fixture()
def sync_method(func, mocker):
    method_name, target_func, args = func

    target = mocker.patch(f'tinvest.clients.{target_func}', autospec=True)
    method = getattr(SyncClient, method_name)

    return method, target, args


def test_sync_client(sync_client, sync_method):
    method, target, args = sync_method

    method(sync_client, *args)

    target.assert_called_once_with(sync_client._request, *args)


def test_default_session(token):
    client = SyncClient(token)

    assert isinstance(client._session, requests.Session)


def test_request(token, session, tracking_id, headers):
    client = SyncClient(token, session=session)

    result = client._request('GET', '/path', Empty, params={'k': 1})

    assert result.tracking_id == tracking_id
    session.request.assert_called_once_with(
        'GET', f'{PRODUCTION}/path', headers=headers, params={'k': 1}
    )


@pytest.mark.usefixtures('_too_many_requests')
def test_request_too_many_requests(token, session):
    client = SyncClient(token, session=session)

    with pytest.raises(TooManyRequestsError):
        client._request('GET', '/path', Empty)


@pytest.mark.usefixtures('_unexpected_error')
def test_request_unexpected_error(token, session):
    client = SyncClient(token, session=session)

    with pytest.raises(UnexpectedError):
        client._request('GET', '/path', Empty)


@pytest.mark.usefixtures('_bad_request')
def test_request_bad_request(token, session):
    client = SyncClient(token, session=session)

    with pytest.raises(BadRequestError):
        client._request('GET', '/path', Empty)
