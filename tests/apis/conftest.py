import pytest


@pytest.fixture()
def http_request(mocker):
    return mocker.Mock()
