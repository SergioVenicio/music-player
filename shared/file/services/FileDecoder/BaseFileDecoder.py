from abc import ABC, abstractclassmethod


class ABCFileDecoder(ABC):
    @abstractclassmethod
    def execute(self, raw_file, file_name):
        raise NotImplementedError()

    @abstractclassmethod
    def analyse_file(self, raw_file):
        raise NotImplementedError()
