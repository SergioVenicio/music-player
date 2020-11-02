from django.apps import AppConfig


class BandConfig(AppConfig):
    name = 'band'

    def ready(self):
        import band.signals  # noqa
