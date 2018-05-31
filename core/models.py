"""
    Modelos do banco de dados
"""
import os
import eyed3
from mutagen.mp3 import MP3
from django.db import models
from music_player.settings import MEDIA_ROOT
from django.dispatch import receiver
from music_player.settings import BASE_DIR
from datetime import timedelta
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save, post_save, post_delete
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """
        Classe de manipulação de usuários
    """
    use_in_migration = True

    def create_user(self, email, password):
        """
            Cria um novo usuário
            :param email: Email do usuário
            :param password: Senha do usuário
            :return: Uma instancia de usuário
        """
        if not email:
            raise ValueError('O e-mail é obrigatorio!')

        if not password:
            raise ValueError('A senha é obrigatória!')

        if len(password) < 6:
            raise ValueError('A senha deve ter pelo menos 6 caracteres!')

        usuario = self.model(
            email=self.normalize_email(email)
        )
        usuario.is_staff = False
        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, email, password):
        """
            Cria um  usuário administrador
            :param email: Email do usuário
            :param password: Senha do usuário
            :return: Uma instancia de usuário administrador
        """
        usuario = self.create_user(email, password)
        usuario.is_admin = True
        usuario.is_staff = True
        usuario.save()
        return usuario


class Usuario(AbstractBaseUser):
    """
        Modelo de usuários
    """
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def is_superuser(self):
        """
            Propriedade que define usuários administradores
        """
        return self.is_admin

    @property
    def is_staff(self):
        """
            Propriedade que define se o usuário pode logar no admin
        """
        return self.is_admin

    def has_perm(self, perm, obj=None):
        """
            Permissões do usuário
        """
        return self.is_admin

    def has_module_perms(self, app_label):
        """
            Permissões do usuário em módulos
        """
        return self.is_admin


class Genero(models.Model):
    """
        Modelo de genero musical
    """
    descricao = models.CharField(max_length=250)

    def __str__(self):
        return self.descricao

    def __repr__(self):
        return f'Genero({self.descricao})'


class Banda(models.Model):
    """
        Modelo de bandas
    """
    nome = models.CharField(max_length=250)
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    def __repr__(self):
        return f'Banda({self.nome}, {self.genero})'


class Album(models.Model):
    """
        Modelo de albuns
    """
    nome = models.CharField(max_length=250)
    banda = models.ForeignKey(Banda, on_delete=models.CASCADE)
    data_lancamento = models.PositiveIntegerField()
    capa = models.ImageField(('Capa'), upload_to='capas', blank=True)

    def __str__(self):
        return self.nome

    def __repr__(self):
        return f'Album(\
            {self.nome}, {self.banda}, {self.data_lancamento}, {self.capa}\
        )'


class Musica(models.Model):
    """
        Modelo de musicas
    """
    nome = models.CharField(max_length=250)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    ordem = models.PositiveIntegerField(null=True)
    arquivo = models.FileField(_('File'), upload_to='musics')
    arquivo_tipo = models.CharField(max_length=10, blank=True)
    duracao = models.DurationField(blank=True, null=True)

    def __str__(self):
        return self.nome

    def __repr__(self):
        return f'Musica(\
            {self.nome}, {self.album}, {self.ordem}, {self.arquivo}\
        )'

    class Meta:
        """ Ordenação utilizando o atributor ordem """
        ordering = ('ordem',)


@receiver(pre_save, sender=Musica)
def change_tipo(sender, instance, **kwargs):
    """
        Altera o tipo do arquivo
    """
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

    instance.arquivo_tipo = arquivo_tipo


@receiver(post_save, sender=Musica)
def get_duration(sender, instance, **kwargs):
    file = eyed3.load(instance.arquivo.path)
    file.initTag()
    file.tag.album = str(instance.album)
    file.tag.artist = str(instance.album.banda.nome)
    file.tag.genre = str(instance.album.banda.genero)
    file.tag.title = str(instance.nome)
    file.tag.track_num = str(instance.ordem)
    file.tag.save()
    duracao = timedelta(seconds=MP3(instance.arquivo.path).info.length)
    Musica.objects.filter(pk=instance.id).update(duracao=duracao)


@receiver(post_delete, sender=Musica)
def apaga_musica(sender, instance, **kwargs):
    """
        Apaga uma musica do hd quando ela for apagada do banco de dados
    """
    try:
        os.remove(os.path.join(MEDIA_ROOT, instance.arquivo.name))
    except FileNotFoundError:
        print('Arquivo não encontrado: {}'.format(
            instance.arquivo.path
        ))


@receiver(post_delete, sender=Album)
def apaga_capa(sender, instance, **kwargs):
    """
        Apaga uma capa do hd quando o album for apagada do banco de dados
    """
    arquivo = os.path.join(BASE_DIR, 'static', str(instance.capa))
    os.remove(arquivo)
