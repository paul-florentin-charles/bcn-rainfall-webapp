import pytest

from bcn_rainfall_webapp.utils.base_config import BaseConfig


class DummyConfig(BaseConfig):
    pass


class TestBaseConfig:
    @staticmethod
    @pytest.fixture
    def monkeypatch():
        patch = pytest.MonkeyPatch()
        # Patch _load_config to avoid file access
        patch.setattr(DummyConfig, "_load_config", lambda self: None)

        return patch

    @staticmethod
    def test_type_error_on_base_instantiation():
        with pytest.raises(TypeError):
            BaseConfig(path="config.yml")

    @staticmethod
    def test_dummy_config_instantiation(monkeypatch):
        assert isinstance(DummyConfig(path="config.yml"), DummyConfig)

    @staticmethod
    def test_reload(monkeypatch):
        DummyConfig._instance = None

        with pytest.raises(RuntimeError):
            DummyConfig.reload()

        inst = DummyConfig(path="config.yml")
        inst.reload()

        assert isinstance(inst, DummyConfig)
