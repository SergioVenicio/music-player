import json

from django.conf import settings

from redis import Redis
from redis.exceptions import ConnectionError

from . import ABCCacheService


class RedisService(ABCCacheService):
    _conn = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PWD,
        db=settings.REDIS_DB
    )

    def get(self, key):
        try:
            return json.loads(self._conn.get(key))
        except (TypeError, ConnectionError):
            return None

    def set(self, key, value: dict):
        data = json.dumps(value)

        try:
            self._conn.set(key, data)
        except ConnectionError:
            return None

    def unset(self, key):
        try:
            self._conn.delete(key)
        except ConnectionError:
            return None

    def update(self, key, value):
        self.unset(key)
        self.set(key, value)

    def flushall(self):
        try:
            self._conn.flushall()
        except ConnectionError:
            return None
