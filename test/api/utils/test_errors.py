from bcn_rainfall_core.utils import Month, Season, TimeMode
from fastapi import HTTPException
from pytest import raises

import bcn_rainfall_webapp.api.utils.errors as http_err


def test_raise_time_mode_error_or_do_nothing():
    assert http_err.raise_time_mode_error_or_do_nothing(TimeMode.YEARLY) is None

    assert (
        http_err.raise_time_mode_error_or_do_nothing(TimeMode.MONTHLY, month=Month.MAY)
        is None
    )

    assert (
        http_err.raise_time_mode_error_or_do_nothing(
            TimeMode.SEASONAL, season=Season.FALL
        )
        is None
    )

    with raises(HTTPException):
        http_err.raise_time_mode_error_or_do_nothing(TimeMode.MONTHLY, month=None)

    with raises(HTTPException):
        http_err.raise_time_mode_error_or_do_nothing(TimeMode.SEASONAL, season=None)


def test_raise_year_related_error_or_do_nothing():
    assert http_err.raise_year_related_error_or_do_nothing(1975, 1995) is None

    with raises(HTTPException):
        http_err.raise_year_related_error_or_do_nothing(1995, 1975)
