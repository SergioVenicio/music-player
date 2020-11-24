from django.apps import AppConfig

from music_player import container

from . import api


class MusicConfig(AppConfig):
    name = 'music'

    def ready(self):
        import music.signals  # noqa
        container.wire(packages=[api])
