import os

from django.db import models
from django.dispatch import receiver
from music_player.settings import BASE_DIR
from django.db.models.signals import post_delete


class Genre(models.Model):
    description = models.CharField(
        max_length=250,
        unique=True
    )
    genre_image = models.ImageField(
        ('Genre'),
        upload_to='images/genres',
        blank=True
    )

    def __str__(self):
        return self.description

    def __repr__(self):
        return f'Genre({self.description})'

    class Meta:
        db_table = 'genre'
        ordering = ('description', 'id',)


class Band(models.Model):
    name = models.CharField(max_length=250, unique=True)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    band_image = models.ImageField(
        ('Band'), upload_to='images/bands', blank=True
    )

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Band({self.name})'

    class Meta:
        db_table = 'band'
        ordering = ('name', 'genre',)


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
