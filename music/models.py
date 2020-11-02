import os

from django.db import models

from album.models import Album


def music_upload(instance, filename):
    from shared.file.services.LocalStorage import LocalStorage

    album = instance.album

    storage = LocalStorage()
    file_name, file_type = os.path.splitext(filename)
    raw_name = ''.join([
        instance.name,
        instance.album.band.name,
        instance.album.band.genre.description,
        file_name
    ])
    path = os.path.join('musics', f'{album.band.name}', f'{album.name}')

    return storage.execute(path, raw_name, file_type)


class Music(models.Model):
    name = models.CharField(max_length=250)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    file = models.FileField(('File'), upload_to=music_upload)
    file_type = models.CharField(max_length=10, blank=True)
    duration = models.DurationField(blank=True, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Music({self.name})'

    class Meta:
        db_table = 'music'
        ordering = ('album', 'order',)
