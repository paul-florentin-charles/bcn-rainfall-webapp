from unittest.mock import patch

import pytest

from bcn_rainfall_webapp.db.client import DBClient


class TestDBClient:
    @staticmethod
    @pytest.fixture
    def db_client():
        with patch("bcn_rainfall_webapp.db.client.Redis") as MockRedis:
            yield DBClient(host="localhost", port=6379, db=0), MockRedis.return_value

    @staticmethod
    def test_set_and_get(db_client):
        client, mock_redis = db_client

        client.enable()
        client._set("foo", "bar")
        mock_redis.set.assert_called()
        mock_redis.get.return_value = "bar"

        result = client._get("foo")
        mock_redis.get.assert_called_with("foo")

        assert result == "bar"

    @staticmethod
    def test_disabled_get_returns_none(db_client):
        client, _ = db_client
        client.disable()

        assert client._get("foo") is None
