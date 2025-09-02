import pytest

from bcn_rainfall_webapp.app import openapi_app
from bcn_rainfall_webapp.views import webapp_blueprint


class TestViewsWebapp:
    @staticmethod
    @pytest.fixture
    def client():
        return openapi_app.test_client()

    @staticmethod
    def test_blueprint_name():
        assert webapp_blueprint.name == "webapp"

    @staticmethod
    def test_rainfall_by_year(client):
        response = client.get("/rainfall_by_year")
        data = response.data.decode("utf-8")

        assert response.status_code == 200
        assert "rainfall_by_year" in data

    @staticmethod
    def test_rainfall_average(client):
        response = client.get("/rainfall_average")
        data = response.data.decode("utf-8")

        assert response.status_code == 200
        assert "rainfall_average" in data

    @staticmethod
    def test_rainfall_relative_distance_to_normal(client):
        response = client.get("/rainfall_relative_distance_to_normal")
        data = response.data.decode("utf-8")

        assert response.status_code == 200
        assert "rainfall_relative_distance_to_normal" in data

    @staticmethod
    def test_years_compared_to_normal(client):
        response = client.get("/years_compared_to_normal")
        data = response.data.decode("utf-8")

        assert response.status_code == 200
        assert "years_compared_to_normal" in data

    @staticmethod
    def test_rainfall_standard_deviation(client):
        response = client.get("/rainfall_standard_deviation")
        data = response.data.decode("utf-8")

        assert response.status_code == 200
        assert "rainfall_standard_deviation" in data
