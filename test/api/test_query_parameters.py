"""Test the query parameters in bcn_rainfall_webapp/api/query_parameters.py."""

import pytest
from pydantic.fields import FieldInfo

from bcn_rainfall_webapp.api.query_parameters import get_pydantic_field


def test_get_pydantic_field():
    field = get_pydantic_field("time_mode")

    assert isinstance(field, FieldInfo)
    assert field.description == "Time mode to filter by"


def test_get_pydantic_field_unknown_key():
    with pytest.raises(KeyError):
        get_pydantic_field("unknown_key")
