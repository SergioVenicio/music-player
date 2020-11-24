from django.apps import AppConfig

from music_player import container


class AlbumConfig(AppConfig):
    name = 'album'

    def ready(self):
        from . import api
        from . import models
        import album.signals  # noqa

        container.wire(packages=[api], modules=[models])
