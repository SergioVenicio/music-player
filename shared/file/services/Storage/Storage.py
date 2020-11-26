from abc import ABC, abstractclassmethod


class ABCStorage(ABC):
    @abstractclassmethod
    def execute(self, path, file_name, file_type):
        raise NotImplementedError()
