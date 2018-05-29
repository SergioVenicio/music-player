import os
from django.db import models
from music_player.settings import MEDIA_ROOT
from django.dispatch import receiver
from music_player.settings import BASE_DIR
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save, post_delete
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migration = True

    def create_user(self, email, password):
        if not email:
            raise ValueError('O e-mail é obrigatorio!')

        if not password:
            raise ValueError('A senha é obrigatória!')

        if len(password) < 6:
            raise ValueError('A senha deve ter pelo menos 6 caracteres!')

        usuario = self.model(
            email=self.normalize_email(email)
        )
        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, email, password):
        usuario = self.create_user(email, password)
        usuario.is_admin = True
        usuario.is_staff = True
        usuario.save()
        return usuario


class Usuario(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin


class Genero(models.Model):
    descricao = models.CharField(max_length=250)

    def __str__(self):
        return self.descricao


class Banda(models.Model):
    nome = models.CharField(max_length=250)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Album(models.Model):
    nome = models.CharField(max_length=250)
    banda = models.ForeignKey(Banda, on_delete=models.CASCADE)
    data_lancamento = models.PositiveIntegerField()
    capa = models.ImageField(('Capa'), upload_to='capas', blank=True)

    def __str__(self):
        return self.nome


class Musica(models.Model):
    nome = models.CharField(max_length=250)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    ordem = models.PositiveIntegerField(null=True)
    arquivo = models.FileField(_('File'), upload_to='musics')
    arquivo_tipo = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ('ordem',)


@receiver(pre_save, sender=Musica)
def change_tipo(sender, instance, **kwargs):
    arquivo_tipo = os.path.splitext(instance.arquivo.name)[1]
    arquivo_tipo = arquivo_tipo[1::].lower()

    if arquivo_tipo == ('mp3' or '.mp3'):
        arquivo_tipo = 'audio/mpeg'
    elif arquivo_tipo == 'ogg':
        arquivo_tipo = 'audio/ogg'
    elif arquivo_tipo == 'wav':
        arquivo_tipo = 'audio/wav'
    else:
        raise ValueError('Tipo de arquivo não permitido!')


@receiver(post_delete, sender=Musica)
def apaga_musica(sender, instance, **kwargs):
    try:
        os.remove(os.path.join(MEDIA_ROOT, instance.arquivo.name))
    except FileNotFoundError:
        print('Arquivo não encontrado: {}'.format(
            instance.arquivo.path
        ))


@receiver(post_delete, sender=Album)
def apaga_capa(sender, instance, **kwargs):
    arquivo = os.path.join(BASE_DIR, 'static', str(instance.capa))
    os.remove(arquivo)
