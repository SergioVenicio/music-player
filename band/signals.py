import os

from django.dispatch import receiver
from music_player.settings import BASE_DIR
from django.db.models.signals import post_delete

from .models import Band, Genre


@receiver(post_delete, sender=Band)
def delete_band_image(sender, instance, **kwargs):
    if instance.band_image:
        _file = os.path.join(BASE_DIR, 'media', str(instance.band_image))
        try:
            os.remove(_file)
        except FileNotFoundError:
            print(f'File not found: {instance.band_image.path}')


@receiver(post_delete, sender=Genre)
def apaga_img_genero(sender, instance, **kwargs):
    if instance.genre_image:
        _file = os.path.join(BASE_DIR, 'media', str(instance.genre_image))
        try:
            os.remove(_file)
        except FileNotFoundError:
            print(f'File not found: {instance.genre_image.path}')
