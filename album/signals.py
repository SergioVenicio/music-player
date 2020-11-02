import os

from django.dispatch import receiver
from music_player.settings import BASE_DIR
from django.db.models.signals import pre_delete

from .models import Album


@receiver(pre_delete, sender=Album)
def delete_cover_image(sender, instance, **kwargs):
    if instance.cover_image:
        _file = os.path.join(BASE_DIR, 'media', str(instance.cover_image))
        try:
            os.remove(_file)
        except FileNotFoundError:
            print(f'Arquivo não encontrado: {instance.cover_image.path}')
