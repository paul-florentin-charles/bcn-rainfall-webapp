import pytest
from fastapi.testclient import TestClient

from bcn_rainfall_webapp.api.app import fastapi_app
from bcn_rainfall_webapp.api.utils import RainfallModel

test_client = TestClient(fastapi_app)


class TestAPP:
    # -- Rainfall data -- #

    @staticmethod
    @pytest.mark.parametrize(
        "time_mode,month,season",
        [
            ("yearly", None, None),
            ("monthly", "May", None),
            ("seasonal", None, "fall"),
        ],
    )
    def test_get_rainfall_average(time_mode, month, season):
        params = {
            "time_mode": time_mode,
            "begin_year": 1978,
            "end_year": 1995,
            "month": month,
            "season": season,
        }

        response = test_client.get(
            "/rainfall/average",
            params={key: value for key, value in params.items() if value is not None},
        )

        assert response.status_code == 200

        data = response.json()
        for key in params:
            assert params[key] == data[key]

        assert RainfallModel(**data) is not None

    @staticmethod
    @pytest.mark.parametrize(
        "time_mode,month,season,begin_year,end_year",
        [
            ("yearly", None, None, 1995, 1978),
            ("monthly", None, "winter", 1978, 1995),
            ("seasonal", "February", None, 1978, 1995),
        ],
    )
    def test_fail_to_get_rainfall_average(
        time_mode, begin_year, end_year, month, season
    ):
        params = {
            "time_mode": time_mode,
            "begin_year": begin_year,
            "end_year": end_year,
            "month": month,
            "season": season,
        }

        response = test_client.get(
            "/rainfall/average",
            params={key: value for key, value in params.items() if value is not None},
        )

        assert response.status_code == 400

    # TODO: Implement similar tests for every route
