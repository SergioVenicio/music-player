import base64

from django.core.files.base import ContentFile


class FileDecoder:
    valid_types = ('jpg', 'jpeg', 'png', 'mp3', 'mpeg')
    parsed_types = {
        'mpeg': 'mp3'
    }

    def execute(self, raw_file, file_name):
        file_type, content = self.analyse_file(raw_file)
        decoded_file = ContentFile(
            content,
            name=f'{file_name}.{file_type}'
        )

        return decoded_file

    def analyse_file(self, raw_file):
        file_header, file_content = raw_file.split(',')
        file_type = file_header.split('/')[1].split(';')[0]

        if file_type not in self.valid_types:
            raise ValueError('Invalid file type!')

        parsed_type = self.parsed_types.get(file_type, file_type)

        return parsed_type, base64.b64decode(file_content)
