from django.apps import AppConfig


class BandConfig(AppConfig):
    name = 'band'

    def ready(self):
        import band.signals  # noqa

        from . import api
        from . import models
        from music_player import container

        container.wire(packages=[api], modules=[models])
