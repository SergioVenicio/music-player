from django.apps import AppConfig

from music_player import container

from . import api


class BandConfig(AppConfig):
    name = 'band'

    def ready(self):
        import band.signals  # noqa
        container.wire(packages=[api])
