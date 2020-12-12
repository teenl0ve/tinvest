from datetime import datetime

import pytest

from tinvest.utils import Func, isoformat, set_default_headers, validate_token


def test_set_default_headers(token):
    data = {}
    set_default_headers(data, token)
    assert data == {
        'headers': {'accept': 'application/json', 'Authorization': f'Bearer {token}'}
    }


def test_set_default_headers_with_headers(token):
    data = {
        'headers': {'Authorization': 'Bearer <OTHER_TOKEN>', 'X-Custom-Header': 'value'}
    }
    set_default_headers(data, token)
    assert data == {
        'headers': {
            'accept': 'application/json',
            'Authorization': 'Bearer <OTHER_TOKEN>',
            'X-Custom-Header': 'value',
        }
    }


@pytest.mark.parametrize(
    ('dt', 'expected'),
    [
        ('2000-01-01T00:00:00+00:00', '2000-01-01T00:00:00+00:00'),
        (datetime(2000, 1, 1), '2000-01-01T00:00:00+00:00'),
    ],
)
def test_isoformat(dt, expected):
    assert isoformat(dt) == expected


@pytest.mark.asyncio
async def test_sync_func(mocker):
    some_sync_func = mocker.Mock(return_value=1)

    assert await Func(some_sync_func, 1, key='')() == 1

    some_sync_func.assert_called_once_with(1, key='')


@pytest.mark.asyncio
async def test_async_func(mocker):
    some_async_func = mocker.AsyncMock(return_value=1)

    assert await Func(some_async_func, 1, key='')() == 1

    some_async_func.assert_called_once_with(1, key='')


def test_validate_token():
    validate_token('token')


def test_invalid_token():
    with pytest.raises(ValueError, match='Token can not be empty'):
        validate_token('')
