from bcn_rainfall_webapp.config import Config

config = Config()


class TestConfig:
    @staticmethod
    def test_get_webapp_server_settings():
        settings = config.get_webapp_server_settings
        for attr in ["host", "port", "debug"]:
            assert hasattr(settings, attr)

    @staticmethod
    def test_get_redis_server_settings():
        settings = config.get_redis_server_settings
        for attr in ["host", "port", "db", "decode_responses"]:
            assert hasattr(settings, attr)

    @staticmethod
    def test_get_fastapi_base_url():
        assert isinstance(config.get_fastapi_base_url, str)
