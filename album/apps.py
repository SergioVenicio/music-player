from django.apps import AppConfig

from music_player import container

from . import api


class AlbumConfig(AppConfig):
    name = 'album'

    def ready(self):
        import album.signals  # noqa
        container.wire(packages=[api])
