import pytest

from tinvest.constants import PRODUCTION, SANDBOX, STREAMING, get_base_url


def test_production():
    assert PRODUCTION == 'https://api-invest.tinkoff.ru/openapi'


def test_sandbox():
    assert SANDBOX == 'https://api-invest.tinkoff.ru/openapi/sandbox'


def test_steaming():
    assert STREAMING == 'wss://api-invest.tinkoff.ru/openapi/md/v1/md-openapi/ws'


@pytest.mark.parametrize(
    ('expected', 'use_sandbox'),
    [
        (PRODUCTION, False),
        (SANDBOX, True),
    ],
)
def test_get_base_url(expected, use_sandbox):
    assert get_base_url(use_sandbox) == expected
