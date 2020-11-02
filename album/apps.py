from django.apps import AppConfig


class AlbumConfig(AppConfig):
    name = 'album'

    def ready(self):
        import album.signals  # noqa
