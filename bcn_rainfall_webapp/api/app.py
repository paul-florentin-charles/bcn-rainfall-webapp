"""
FastAPI application exposing API routes related to rainfall data of Barcelona.
"""

from typing import Any, Callable

from fastapi import FastAPI


class FastAPPI(FastAPI):
    """Overrides FastAPI class to initiate our own app."""

    def __init__(self, **kwargs):
        from bcn_rainfall_webapp.api.routes import (
            ROUTER_BY_NAME,
            get_endpoint_to_api_route_specs_by_router_name,
        )

        super().__init__(**kwargs)

        for (
            router_name,
            endpoint_to_api_route_specs,
        ) in get_endpoint_to_api_route_specs_by_router_name().items():
            router = ROUTER_BY_NAME[router_name]
            for endpoint, api_route_specs in endpoint_to_api_route_specs.items():
                router.add_api_route(
                    endpoint=endpoint,
                    **api_route_specs.model_dump(),
                )

            self.include_router(router)

    @classmethod
    def from_config(cls, path="config.yml"):
        from bcn_rainfall_webapp import Config
        from bcn_rainfall_webapp.api.routes import (
            MAX_YEAR_AVAILABLE,
            MIN_YEAR_AVAILABLE,
        )

        return cls(
            **Config(path=path).get_api_settings.fastapi.model_dump(),
            description=f"Available data is between {MIN_YEAR_AVAILABLE} and {MAX_YEAR_AVAILABLE}.",
        )

    def add_api_route(
        self,
        path: str,
        endpoint: Callable[..., Any],
        **kwargs,
    ):
        kwargs.setdefault("methods", ["GET"])
        kwargs.setdefault("operation_id", endpoint.__name__.title().replace("_", ""))

        super().add_api_route(path, endpoint, **kwargs)


fastapi_app = FastAPPI.from_config()
