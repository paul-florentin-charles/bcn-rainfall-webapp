import pytest
from bcn_rainfall_core.utils import Month, Season, TimeMode
from werkzeug.exceptions import HTTPException

from bcn_rainfall_webapp.api.utils import (
    RainfallModel,
    raise_time_mode_error_or_do_nothing,
    raise_year_related_error_or_do_nothing,
)


def test_rainfall_model():
    model = RainfallModel(
        name="test",
        value=10.0,
        begin_year=2000,
        end_year=2001,
    )

    assert model.name == "test"
    assert model.value == 10.0
    assert model.begin_year == 2000
    assert model.end_year == 2001


def test_raise_time_mode_error_or_do_nothing():
    # Should raise an exception
    with pytest.raises(HTTPException):
        raise_time_mode_error_or_do_nothing(time_mode=TimeMode.MONTHLY)
    with pytest.raises(HTTPException):
        raise_time_mode_error_or_do_nothing(time_mode=TimeMode.SEASONAL)

    # Should not raise an exception
    raise_time_mode_error_or_do_nothing(time_mode=TimeMode.YEARLY)
    raise_time_mode_error_or_do_nothing(time_mode=TimeMode.MONTHLY, month=Month.JANUARY)
    raise_time_mode_error_or_do_nothing(
        time_mode=TimeMode.SEASONAL, season=Season.WINTER
    )


def test_raise_year_related_error_or_do_nothing():
    # Should raise an exception
    with pytest.raises(HTTPException):
        raise_year_related_error_or_do_nothing(begin_year=2001, end_year=2000)

    # Should not raise an exception
    raise_year_related_error_or_do_nothing(begin_year=2000, end_year=2001)
    raise_year_related_error_or_do_nothing(begin_year=2000, end_year=2000)
