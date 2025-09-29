from bcn_rainfall_webapp.utils.schemas import (
    DevelopmentServerSettings,
    RedisServerSettings,
)


class TestUtilsSchemas:
    @staticmethod
    def test_webapp_server_settings_fields():
        webapp_settings = DevelopmentServerSettings(host="127.0.0.1", port=5000)

        assert webapp_settings.host == "127.0.0.1"
        assert webapp_settings.port == 5000
        assert webapp_settings.debug is None

    @staticmethod
    def test_redis_server_settings_fields():
        redis_settings = RedisServerSettings(
            host="localhost",
            port=6379,
        )

        assert redis_settings.host == "localhost"
        assert redis_settings.port == 6379
        assert redis_settings.db == 0
