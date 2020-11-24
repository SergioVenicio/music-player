import os

class LocalStorage:
    def __init__(self, hash_service):
        self.hash_service = hash_service()

    def _clean_file_type(self, _type):
        return _type.replace('.', '').replace(',', '').replace(';', '')

    def execute(self, path, file_name, file_type):
        md5_name = self.hash_service.execute(file_name)
        _file = f'{md5_name}.{self._clean_file_type(file_type)}'

        return os.path.join(path, _file)
