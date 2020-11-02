import os

from django.db import models
from django.dispatch import receiver
from music_player.settings import BASE_DIR
from django.db.models.signals import post_delete

from band.models import Band


class Album(models.Model):
    name = models.CharField(
        max_length=250,
        blank=False,
        null=False
    )
    band = models.ForeignKey(
        Band,
        blank=False,
        null=False,
        on_delete=models.CASCADE
    )
    release_date = models.PositiveIntegerField(blank=False, null=False)
    cover_image = models.ImageField(
        ('Cover image'),
        upload_to='images/covers'
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Album({self.name})'

    class Meta:
        db_table = 'album'
        ordering = ('name', 'band', 'release_date',)


@receiver(post_delete, sender=Album)
def delete_cover_image(sender, instance, **kwargs):
    if instance.cover_image:
        _file = os.path.join(BASE_DIR, 'media', str(instance.cover_image))
        try:
            os.remove(_file)
        except FileNotFoundError:
            print(f'Arquivo não encontrado: {instance.cover_image.path}')
