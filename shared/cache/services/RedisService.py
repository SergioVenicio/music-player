import json

from redis import Redis

from django.conf import settings

from .CacheService import CacheService


class RedisService(CacheService):
    __conn = Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PWD,
        db=settings.REDIS_DB
    )

    def get(self, key):
        try:
            return json.loads(self.__conn.get(key))
        except TypeError:
            return None

    def set(self, key, value: dict):
        data = json.dumps(value)
        self.__conn.set(key, data)

    def unset(self, key):
        self.__conn.delete(key)

    def update(self, key, value):
        self.unset(key)
        self.set(key, value)
