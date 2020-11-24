from django.apps import AppConfig

from music_player import container


class BandConfig(AppConfig):
    name = 'band'

    def ready(self):
        import band.signals  # noqa

        from . import api
        from . import models

        container.wire(packages=[api], modules=[models])

