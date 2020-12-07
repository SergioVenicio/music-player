import os

from django.dispatch import receiver
from music_player.settings import BASE_DIR
from django.db.models.signals import post_save, post_delete

from .models import Band, Genre

from dependency_injector.wiring import inject, Provide
from music_player.containers import Container

from shared.cache.services import ABCCacheService


@receiver(post_save, sender=Band)
@inject
def reset_cache(
        sender,
        instance,
        cache: ABCCacheService = Provide[Container.cache_service],
        **kwargs
):
    cache_keys = ['bands', f'bands:genre_id@{instance.genre_id}']
    map(cache.unset, cache_keys)
    return


@receiver(post_delete, sender=Band)
def delete_band_image(sender, instance, **kwargs):
    if instance.band_image:
        _file = os.path.join(BASE_DIR, 'media', str(instance.band_image))
        try:
            os.remove(_file)
        except FileNotFoundError:
            print(f'File not found: {instance.band_image.path}')


@receiver(post_delete, sender=Genre)
def delete_genre_img(sender, instance, **kwargs):
    if instance.genre_image:
        _file = os.path.join(BASE_DIR, 'media', str(instance.genre_image))
        try:
            os.remove(_file)
        except FileNotFoundError:
            print(f'File not found: {instance.genre_image.path}')
