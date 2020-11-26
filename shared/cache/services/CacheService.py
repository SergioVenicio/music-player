from abc import ABC, abstractmethod


class ABCCacheService(ABC):
    @abstractmethod
    def get(self, key: str):
        raise NotImplementedError()

    @abstractmethod
    def set(self, key: str, value: dict):
        raise NotImplementedError()

    @abstractmethod
    def unset(self, key: str):
        raise NotImplementedError()

    @abstractmethod
    def update(self, key: str, value: dict):
        raise NotImplementedError()
