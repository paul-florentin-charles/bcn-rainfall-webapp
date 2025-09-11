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
    def test_get_api_settings():
        settings = config.get_api_settings
        for attr in ["root_path", "title", "summary"]:
            assert hasattr(settings, attr)
