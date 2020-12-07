from django.apps import AppConfig


class BandConfig(AppConfig):
    name = 'band'

    def ready(self):
        from . import signals
        from . import api
        from . import models
        from music_player import container

        container.wire(
            packages=[api],
            modules=[models, signals]
        )
