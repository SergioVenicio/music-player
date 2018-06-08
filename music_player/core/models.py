"""
    Modelos do banco de dados
"""
import os
import eyed3
from mutagen.mp3 import MP3
from django.db import models
from datetime import timedelta
from django.dispatch import receiver
from mutagen.wavpack import WavPackInfo
from music_player.settings import BASE_DIR
from music_player.settings import MEDIA_ROOT
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save, post_save, post_delete
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,\
                                       PermissionsMixin


class UserManager(BaseUserManager):
    """
        Classe de manipulação de usuários
    """
    use_in_migration = True

    def create_user(self, email, nome, sobrenome, password, avatar=None):
        """
            Cria um novo usuário
            :param email: Email do usuário
            :param nome: Nome do usuário
            :param sobrenome: Sobrenome do usuário
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
            email=self.normalize_email(email),
            nome=nome, sobrenome=sobrenome, avatar=avatar
        )
        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, email, nome, sobrenome, password, avatar=None):
        """
            Cria um  usuário administrador
            :param email: Email do usuário
            :param password: Senha do usuário
            :return: Uma instancia de usuário administrador
        """
        usuario = self.create_user(email, nome, sobrenome, password, avatar)
        usuario.is_admin = True
        usuario.save()
        return usuario


def upload_avatar(instance, filename):
    nome = instance.nome
    email = instance.email
    return f"images/usuarios/{nome}_{email}"


class Usuario(AbstractBaseUser, PermissionsMixin):
    """
        Modelo de usuários
    """
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=50)
    sobrenome = models.CharField(max_length=50)
    avatar = models.ImageField(
        ('Avatar'), upload_to=upload_avatar, blank=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'sobrenome']

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

    class Meta:
        ordering = ('email', 'nome', 'sobrenome',)


class Genero(models.Model):
    """
        Modelo de genero musical
    """
    descricao = models.CharField(max_length=250)
    imagen = models.ImageField(
        ('Genero'), upload_to='images/generos', blank=True
    )

    def __str__(self):
        return self.descricao

    def __repr__(self):
        return f'Genero({self.descricao})'

    class Meta:
        ordering = ('descricao', 'id',)


class Banda(models.Model):
    """
        Modelo de bandas
    """
    nome = models.CharField(max_length=250)
    imagen = models.ImageField(
        ('Banda'), upload_to='images/bandas', blank=True
    )
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    def __repr__(self):
        return f'Banda({self.nome}, {self.genero})'

    class Meta:
        ordering = ('nome', 'genero',)


class Album(models.Model):
    """
        Modelo de albuns
    """
    nome = models.CharField(max_length=250)
    banda = models.ForeignKey(Banda, on_delete=models.CASCADE)
    data_lancamento = models.PositiveIntegerField()
    capa = models.ImageField(('Capa'), upload_to='images/capas')

    def __str__(self):
        return self.nome

    def __repr__(self):
        return f'Album(\
            {self.nome}, {self.banda}, {self.data_lancamento}, {self.capa}\
        )'

    class Meta:
        ordering = ('nome', 'banda', 'data_lancamento',)


def upload_musica(instance, filename):
    album = instance.album
    return f"musics/{album.banda.nome}/{album.nome}/{filename}"


class Musica(models.Model):
    """
        Modelo de musicas
    """
    nome = models.CharField(max_length=250)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    ordem = models.PositiveIntegerField(null=True)
    arquivo = models.FileField(_('File'), upload_to=upload_musica)
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
        ordering = ('album', 'ordem',)


@receiver(pre_save, sender=Musica)
def change_tipo(sender, instance, **kwargs):
    """
        Altera o tipo do arquivo
    """
    arquivo_tipo = os.path.splitext(instance.arquivo.name)[1]
    arquivo_tipo = arquivo_tipo[1::].lower()

    if arquivo_tipo == ('mp3' or '.mp3'):
        arquivo_tipo = 'audio/mpeg'
    else:
        raise ValueError('Tipo de arquivo não permitido!')

    instance.arquivo_tipo = arquivo_tipo


@receiver(post_save, sender=Musica)
def get_duration(sender, instance, **kwargs):
    try:
        file = eyed3.load(instance.arquivo.path)
        file.initTag()
    except AttributeError:
        print('Não foi possivel escrever os metadados')
    else:
        file.tag._se = None
        file.tag.album = str(instance.album)
        file.tag.artist = str(instance.album.banda.nome)
        file.tag.genre = str(instance.album.banda.genero)
        file.tag.title = str(instance.nome)
        file.tag.track_num = str(instance.ordem)
        file.tag.save()

    if instance.arquivo_tipo == 'audio/mpeg':
        duracao = timedelta(seconds=MP3(instance.arquivo.path).info.length)
    elif instance.arquivo_tipo == 'audio/wav':
        duracao = timedelta(
            seconds=WavPackInfo(instance.arquivo.path).info.length
        )
    Musica.objects.filter(pk=instance.id).update(duracao=duracao)


@receiver(post_delete, sender=Musica)
def apaga_musica(sender, instance, **kwargs):
    """
        Apaga uma musica do hd quando ela for apagada do banco de dados
    """
    try:
        os.remove(
            os.path.join(
                MEDIA_ROOT,
                instance.arquivo.path
            )
        )
    except FileNotFoundError:
        print('Arquivo não encontrado: {}'.format(
            instance.arquivo.path
        ))


@receiver(post_delete, sender=Album)
def apaga_capa(sender, instance, **kwargs):
    """
        Apaga uma capa do hd quando o album for apagada do banco de dados
    """
    arquivo = os.path.join(BASE_DIR, 'media', str(instance.capa))
    os.remove(arquivo)


@receiver(post_delete, sender=Genero)
def apaga_img_genero(sender, instance, **kwargs):
    """
        Apaga a imagen de um genero quando ele for deletado do banco de dados
    """
    arquivo = os.path.join(BASE_DIR, 'media', str(instance.imagen))
    os.remove(arquivo)
