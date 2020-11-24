import os

from django.db import models

from shared.file.services.LocalStorage import LocalStorage


def upload_band_image(instance, filename):
    storage = LocalStorage()

    file_name, file_type = os.path.splitext(filename)

    raw_name = ''.join([
        instance.name,
        instance.genre.description,
        file_name
    ])

    return storage.execute('images/bands', raw_name, file_type)


def upload_genre_image(instance, filename):
    storage = LocalStorage()

    file_name, file_type = os.path.splitext(filename)

    raw_name = ''.join([
        instance.description,
        file_name
    ])

    return storage.execute('images/genres', raw_name, file_type)


class Genre(models.Model):
    description = models.CharField(
        max_length=250,
        unique=True
    )
    genre_image = models.ImageField(
        ('Genre'),
        upload_to=upload_genre_image,
        blank=True
    )

    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'genre_image': str(self.genre_image)
        }

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
        ('Band'), upload_to=upload_band_image, blank=True
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'genre': self.genre.to_dict(),
            'band_image': str(self.band_image.url)
        }

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Band({self.name})'

    class Meta:
        db_table = 'band'
        ordering = ('name', 'genre',)
