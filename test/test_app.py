import pytest

from bcn_rainfall_webapp.app import openapi_app


class TestFlaskApp:
    @staticmethod
    @pytest.fixture
    def client():
        return openapi_app.test_client()

    @staticmethod
    def test_index(client):
        response = client.get("/")
        data = response.data.decode("utf-8")

        assert response.status_code == 200
        assert "BarnaPluja" in data
