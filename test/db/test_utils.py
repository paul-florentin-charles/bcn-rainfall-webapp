from bcn_rainfall_webapp.db.utils import get_hash_key, get_seconds_until_end_of_the_day


class TestDBUtils:
    @staticmethod
    def test_get_hash_key():
        hash1 = get_hash_key(a=1, b=2)
        hash2 = get_hash_key(b=2, a=1)

        assert hash1 == hash2  # Order shouldn't matter
        assert isinstance(hash1, str)
        assert len(hash1) == 64  # SHA256 hash length

    @staticmethod
    def test_get_seconds_until_end_of_the_day():
        seconds = get_seconds_until_end_of_the_day()

        assert isinstance(seconds, int)
        assert 0 < seconds < 86400
