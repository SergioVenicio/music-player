import os

from django.dispatch import receiver
from music_player.settings import BASE_DIR
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save, post_delete

from .models import User


@receiver(post_delete, sender=User)
def delete_user_avatar(sender, instance, **kwargs):
    if instance.avatar:
        _file = os.path.join(BASE_DIR, 'media', str(instance.avatar))
        try:
            os.remove(_file)
        except FileNotFoundError:
            print(f'File not found: {instance.avatar.path}')


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
