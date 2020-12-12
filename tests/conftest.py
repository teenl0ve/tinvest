# pylint:disable=redefined-outer-name
import pytest


@pytest.fixture()
def token():
    return '<TOKEN>'


@pytest.fixture()
def figi():
    return 'BBG0013HGFT4'


@pytest.fixture()
def request_id():
    return '123ASD1123'


@pytest.fixture()
def broker_account_id():
    return 'some_broker_account_id'


@pytest.fixture()
def tracking_id():
    return 'tracking_id'


@pytest.fixture()
def headers(token):
    return {'Authorization': f'Bearer {token}', 'accept': 'application/json'}
