import pytest

from ..src.redis_storage import RedisTimeSeriesStorage


@pytest.fixture
def redis_storage() -> RedisTimeSeriesStorage:
    storage = RedisTimeSeriesStorage()
    return storage
