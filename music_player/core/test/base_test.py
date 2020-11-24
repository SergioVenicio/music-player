from django.urls import reverse, resolve
from django.test import TestCase

from rest_framework.test import APIClient

from user.models import User

from music_player.containers import Container
from music_player import settings


class BaseTest(TestCase):
    def setUp(self):
        container = Container()
        container.config.from_dict(settings.__dict__)
        self.user = User(
            email='test@test.com',
            name='test',
            last_name='test',
            password='my_test_password'
        )

    def tearDown(self):
        self.user.delete()

    def _get_image(self):
        from shared.file.services.FileDecoder.FileDecoder import FileDecoder

        file_decoder = FileDecoder()

        return file_decoder.execute(
            self._get_raw_image(),
            file_name='test.png'
        )

    def _get_raw_image(self):
        import base64

        file_header = 'data:image/png;base64'
        file_path = 'music_player/core/test/test.png'
        with open(file_path, 'rb') as img_file:
            content = str(base64.b64encode(img_file.read()))

        return f'{file_header},{content}'


class HttpBaseClass(TestCase):
    def setUp(self):
        self.anonymous_client = APIClient()
        self.api_client = APIClient()
        self.api_client.force_authenticate(user=self.user)

    def get_url(self, url):
        return reverse(resolve(url).url_name)
