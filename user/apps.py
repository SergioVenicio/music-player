from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'

    def ready(self):
        import user.signals  # noqa

        from . import api
        from . import models
        from music_player import container

        container.wire(packages=[api], modules=[models])
