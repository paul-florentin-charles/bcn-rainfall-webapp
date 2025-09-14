import os

from bcn_rainfall_core.utils import Season, TimeMode
from redis import Redis

from bcn_rainfall_webapp.db.utils import get_hash_key, get_seconds_until_end_of_the_day


class DBClient:
    def __init__(self, host: str, port: int, db: int, **kwargs):
        self.client = Redis(host=host, port=port, db=db, **kwargs)
        self.host = host
        self.port = port
        self.db = db

        self.enabled = True

    @classmethod
    def from_config(cls, path="config.yml"):
        from bcn_rainfall_webapp.config import Config

        # Use env vars set in docker-compose.yml
        redis_settings = Config(path=path).get_redis_server_settings
        if env__redis_host := os.getenv("REDIS_HOST"):
            redis_settings.host = env__redis_host
        if env__redis_port := os.getenv("REDIS_PORT"):
            redis_settings.port = int(env__redis_port)

        return cls(**redis_settings.model_dump())

    def disable(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def _get(self, key: str) -> str | None:
        if not self.enabled:
            return None

        return self.client.get(key)

    def _set(self, key: str, value: str, **kwargs):
        if not self.enabled:
            return

        # Default TTL is until the end of the day
        kwargs.setdefault("ex", get_seconds_until_end_of_the_day())

        self.client.set(key, value, **kwargs)

    def get_rainfall_by_year_as_plotly_json(
        self,
        *,
        time_mode: TimeMode,
        begin_year: int,
        end_year: int,
        **kwargs,
    ) -> str | None:
        return self._get(
            get_hash_key(
                name="rainfall_by_year_as_plotly_json",
                time_mode=time_mode.value,
                begin_year=begin_year,
                end_year=end_year,
                **kwargs,
            )
        )

    def set_rainfall_by_year_as_plotly_json(
        self,
        *,
        time_mode: TimeMode,
        begin_year: int,
        end_year: int,
        data: str,
        **kwargs,
    ):
        self._set(
            get_hash_key(
                name="rainfall_by_year_as_plotly_json",
                time_mode=time_mode.value,
                begin_year=begin_year,
                end_year=end_year,
                **kwargs,
            ),
            data,
        )

    def get_seasonal_rainfall_as_plotly_json(
        self, *, season: Season, begin_year: int, end_year: int
    ) -> str | None:
        return self._get(
            get_hash_key(
                name="seasonal_rainfall_as_plotly_json",
                season=season.value,
                begin_year=begin_year,
                end_year=end_year,
            )
        )

    def set_seasonal_rainfall_as_plotly_json(
        self,
        *,
        season: Season,
        begin_year: int,
        end_year: int,
        data: str,
    ):
        self._set(
            get_hash_key(
                name="seasonal_rainfall_as_plotly_json",
                season=season.value,
                begin_year=begin_year,
                end_year=end_year,
            ),
            data,
        )

    def get_rainfall_averages_as_plotly_json(
        self,
        *,
        time_mode: TimeMode,
        begin_year: int,
        end_year: int,
    ):
        return self._get(
            get_hash_key(
                name="rainfall_averages_as_plotly_json",
                time_mode=time_mode.value,
                begin_year=begin_year,
                end_year=end_year,
            )
        )

    def set_rainfall_averages_as_plotly_json(
        self,
        *,
        time_mode: TimeMode,
        begin_year: int,
        end_year: int,
        data: str,
    ):
        self._set(
            get_hash_key(
                name="rainfall_averages_as_plotly_json",
                time_mode=time_mode.value,
                begin_year=begin_year,
                end_year=end_year,
            ),
            data,
        )

    def get_rainfall_linreg_slopes_as_plotly_json(
        self,
        *,
        time_mode: TimeMode,
        begin_year: int,
        end_year: int,
    ):
        return self._get(
            get_hash_key(
                name="rainfall_linreg_slopes_as_plotly_json",
                time_mode=time_mode.value,
                begin_year=begin_year,
                end_year=end_year,
            )
        )

    def set_rainfall_linreg_slopes_as_plotly_json(
        self,
        *,
        time_mode: TimeMode,
        begin_year: int,
        end_year: int,
        data: str,
    ):
        self._set(
            get_hash_key(
                name="rainfall_linreg_slopes_as_plotly_json",
                time_mode=time_mode.value,
                begin_year=begin_year,
                end_year=end_year,
            ),
            data,
        )

    def get_relative_distances_to_rainfall_normal_as_plotly_json(
        self,
        *,
        time_mode: TimeMode,
        normal_year: int,
        begin_year: int,
        end_year: int,
    ):
        return self._get(
            get_hash_key(
                name="relative_distances_to_rainfall_normal_as_plotly_json",
                time_mode=time_mode.value,
                normal_year=normal_year,
                begin_year=begin_year,
                end_year=end_year,
            )
        )

    def set_relative_distances_to_rainfall_normal_as_plotly_json(
        self,
        *,
        time_mode: TimeMode,
        normal_year: int,
        begin_year: int,
        end_year: int,
        data: str,
    ):
        self._set(
            get_hash_key(
                name="relative_distances_to_rainfall_normal_as_plotly_json",
                time_mode=time_mode.value,
                normal_year=normal_year,
                begin_year=begin_year,
                end_year=end_year,
            ),
            data,
        )

    def get_rainfall_standard_deviations_as_plotly_json(
        self,
        *,
        time_mode: TimeMode,
        begin_year: int,
        end_year: int,
        weigh_by_average=False,
    ):
        return self._get(
            get_hash_key(
                name="rainfall_standard_deviations_as_plotly_json",
                time_mode=time_mode.value,
                begin_year=begin_year,
                end_year=end_year,
                weigh_by_average=weigh_by_average,
            )
        )

    def set_rainfall_standard_deviations_as_plotly_json(
        self,
        *,
        time_mode: TimeMode,
        begin_year: int,
        end_year: int,
        data: str,
        weigh_by_average=False,
    ):
        self._set(
            get_hash_key(
                name="rainfall_standard_deviations_as_plotly_json",
                time_mode=time_mode.value,
                begin_year=begin_year,
                end_year=end_year,
                weigh_by_average=weigh_by_average,
            ),
            data,
        )

    def get_percentage_of_years_compared_to_normal_as_plotly_json(
        self,
        *,
        time_mode: TimeMode,
        normal_year: int,
        begin_year: int,
        end_year: int,
        **kwargs,
    ):
        return self._get(
            get_hash_key(
                name="percentage_of_years_compared_to_normal_as_plotly_json",
                time_mode=time_mode.value,
                normal_year=normal_year,
                begin_year=begin_year,
                end_year=end_year,
                **kwargs,
            )
        )

    def set_percentage_of_years_compared_to_normal_as_plotly_json(
        self,
        *,
        time_mode: TimeMode,
        normal_year: int,
        begin_year: int,
        end_year: int,
        data: str,
        **kwargs,
    ):
        self._set(
            get_hash_key(
                name="percentage_of_years_compared_to_normal_as_plotly_json",
                time_mode=time_mode.value,
                normal_year=normal_year,
                begin_year=begin_year,
                end_year=end_year,
                **kwargs,
            ),
            data,
        )
