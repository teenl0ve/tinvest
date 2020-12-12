# pylint:disable=redefined-outer-name
import json

import pytest

from tinvest.exceptions import BadRequestError, UnexpectedError


@pytest.fixture()
def error_raw(tracking_id):
    return json.dumps(
        {
            'trackingId': tracking_id,
            'payload': {},
        }
    )


def test_bad_request_error(error_raw, tracking_id):
    error = BadRequestError(error_raw)

    assert error.response.tracking_id == tracking_id


def test_unexpected_error():
    error = UnexpectedError(500, 'error')

    assert error.status == 500
    assert error.text == 'error'
