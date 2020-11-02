import os

from django.db import models
from django.dispatch import receiver
from music_player.settings import BASE_DIR
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager
from music.models import Music


def upload_avatar(instance, _):
    name = instance.name
    email = instance.email
    return f"images/users/{name}_{email}"


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
        return f'{self.user.id}, {self.music.id}'

    def __repr__(self):
        return f'Like({self.user.id}, {self.music.id})'

    class Meta:
        db_table = 'like'
        ordering = ('date', 'user', 'music')


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
