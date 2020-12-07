from django.apps import AppConfig


class AlbumConfig(AppConfig):
    name = 'album'

    def ready(self):
        from . import signals
        from . import api
        from . import models
        from music_player import container

        container.wire(
            packages=[api],
            modules=[models, signals]
        )
