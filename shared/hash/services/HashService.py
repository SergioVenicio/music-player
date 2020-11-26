from abc import ABC, abstractmethod


class ABCHashService(ABC):
    @abstractmethod
    def __init__(self, hasher):
        raise NotImplementedError()

    @abstractmethod
    def execute(self, text: str):
        raise NotImplementedError()
