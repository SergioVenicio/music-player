import os

from django.db import models

from band.models import Band


def upload_cover_image(instance, filename):
    from shared.file.services.LocalStorage import LocalStorage

    storage = LocalStorage()

    file_name, file_type = os.path.splitext(filename)

    raw_name = ''.join([
        instance.name,
        instance.band.name,
        str(instance.release_date),
        file_name
    ])

    return storage.execute('images/covers', raw_name, file_type)


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
        upload_to=upload_cover_image
    )

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'band': self.band.to_dict(),
            'release_date': self.release_date,
            'cover_image': str(self.cover_image)
        }

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Album({self.name})'

    class Meta:
        db_table = 'album'
        ordering = ('release_date', 'band', 'name')
