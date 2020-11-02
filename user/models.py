import os

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager
from music.models import Music


def upload_avatar(instance, filename):
    from shared.file.services.LocalStorage import LocalStorage

    storage = LocalStorage()

    file_name, file_type = os.path.splitext(filename)
    raw_text = ''.join([
        instance.name,
        instance.email,
        file_name
    ])
    return storage.execute("images/users/", raw_text, file_type)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    avatar = models.ImageField(
        ('Avatar'), upload_to=upload_avatar, blank=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name']

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        db_table = 'user'
        ordering = ('email', 'name', 'last_name',)


class Like(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.name}, {self.music.name}'

    def __repr__(self):
        return f'Like({self.user.id}, {self.music.id})'

    class Meta:
        db_table = 'like'
        unique_together = (('user', 'music'),)
        ordering = ('date', 'user', 'music')
