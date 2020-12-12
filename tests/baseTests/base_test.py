from django.core.files.base import ContentFile
from django.urls import reverse, resolve
from django.test import TestCase

from rest_framework.test import APIClient

from user.models import User

from music_player.containers import Container
from music_player import settings

from shared.cache.services.RedisService import RedisService


class BaseTest(TestCase):
    def setUp(self):
        container = Container()
        container.config.from_dict(settings.__dict__)

        self.cache = RedisService()

        self.user = User(
            email='test@test.com',
            name='test',
            last_name='test',
            password='my_test_password'
        )

        self.user.save()

    def tearDown(self):
        self.user.delete()
        self.cache.flushall()

    def _get_image(self):
        from shared.file.services.FileDecoder import ImageDecoder

        file_decoder = ImageDecoder()

        return file_decoder.execute(
            self._get_raw_image(),
            file_name='test.png'
        )

    def _get_raw_image(self):
        import base64

        file_header = 'data:image/png;base64'
        file_path = 'tests/baseTests/test.png'
        with open(file_path, 'rb') as img_file:
            content = str(base64.b64encode(img_file.read()))

        return f'{file_header},{content}'

    def _get_raw_mp3(self):
        import base64

        file_header = 'data:audio/mpeg;base64'
        file_path = 'tests/baseTests/music_test.mp3'
        with open(file_path, 'rb') as mp3_file:
            content = base64.b64encode(mp3_file.read())[1:]

        return f'{file_header},{content}'

    def _get_mp3(self):
        import base64

        file_path = 'tests/baseTests/music_test.mp3'
        with open(file_path, 'rb') as mp3_file:
            content = base64.b64encode(mp3_file.read())

        return ContentFile(
            base64.b64decode(content), 'test.mp3'
        )


class HttpBaseClass(TestCase):
    def setUp(self):
        self.anonymous_client = APIClient()
        self.api_client = APIClient()
        self.api_client.force_authenticate(user=self.user)

    def get_reverse_url(self, viewname, pk):
        return reverse(viewname, args=[pk])

    def get_url(self, url, pk=None):
        if pk is None:
            return reverse(resolve(url).url_name)

        return reverse(resolve(url + f'/{pk}/').url_name)
