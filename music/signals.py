import os
from datetime import timedelta

from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
import eyed3
from mutagen.mp3 import MP3
from mutagen.wavpack import WavPackInfo

from .models import Music
from music_player.settings import MEDIA_ROOT


@receiver(pre_save, sender=Music)
def change_music_type(sender, instance, **kwargs):
    file_type = os.path.splitext(instance.file.name)[1]
    parsed_file_type = file_type[1::].lower()

    if parsed_file_type == ('mp3' or '.mp3'):
        new_file_type = 'audio/mpeg'
    else:
        raise ValueError('File type not allowed!')

    instance.file_type = new_file_type


@receiver(post_save, sender=Music)
def get_duration(sender, instance, **kwargs):
    try:
        file = eyed3.load(instance.arquivo.path)
        file.initTag()
    except AttributeError:
        print('Cant write file metadata!')
    else:
        file.tag._se = None
        file.tag.album = str(instance.album)
        file.tag.artist = str(instance.album.band.name)
        file.tag.genre = str(instance.album.band.genre)
        file.tag.title = str(instance.name)
        file.tag.track_num = str(instance.order)
        file.tag.save()

    if instance.file_type == 'audio/mpeg':
        duration = timedelta(seconds=MP3(instance.file.path).info.length)
    else:
        duration = timedelta(
            seconds=WavPackInfo(instance.file.path).info.length
        )

    Music.objects.filter(pk=instance.id).update(duration=duration)


@receiver(post_delete, sender=Music)
def delete_music(sender, instance, **kwargs):
    try:
        os.remove(
            os.path.join(MEDIA_ROOT, instance.file.path)
        )
    except FileNotFoundError:
        print(f'File not found: {instance.file.path}')
