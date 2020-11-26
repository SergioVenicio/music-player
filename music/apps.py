from django.apps import AppConfig


class MusicConfig(AppConfig):
    name = 'music'

    def ready(self):
        import music.signals  # noqa

        from . import api
        from . import models
        from music_player import container

        container.wire(packages=[api], modules=[models])
