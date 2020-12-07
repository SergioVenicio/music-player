import os

from django.dispatch import receiver
from music_player.settings import BASE_DIR
from django.db.models.signals import post_save, pre_delete

from dependency_injector.wiring import inject, Provide
from music_player.containers import Container

from shared.cache.services import ABCCacheService

from .models import Album


@receiver(post_save, sender=Album)
@inject
def reset_cache(
    sender,
    instance,
    cache: ABCCacheService = Provide[Container.cache_service],
    **kwargs
):
    cache.unset('albuns')
    cache.set(f'album@{instance.id}', instance.to_dict())
    return


@receiver(pre_delete, sender=Album)
def delete_cover_image(sender, instance, **kwargs):
    if instance.cover_image:
        _file = os.path.join(BASE_DIR, 'media', str(instance.cover_image))
        try:
            os.remove(_file)
        except FileNotFoundError:
            print(f'Arquivo não encontrado: {instance.cover_image.path}')
