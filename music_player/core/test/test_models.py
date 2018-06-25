import pytest
from music_player.core import models
from django.core.files.base import ContentFile


@pytest.mark.django_db(transaction=True)
def test_user(capa):
    s_user = models.UserManager()
    s_user = s_user.create_user(
        'teste@teste.com', 'teste', 'testando', 'password', capa
    )
    assert s_user is not None
    assert not s_user.is_admin
    assert not s_user.is_superuser
    assert not s_user.is_staff
    assert s_user.nome == 'teste'
    assert s_user.sobrenome == 'testando'
    assert s_user.email == 'teste@teste.com'
    assert s_user.password != 'password'
    assert s_user.delete()


@pytest.mark.django_db(transaction=True)
def test_superuser(capa):
    s_user = models.UserManager()
    s_user = s_user.create_superuser(
        'teste@teste.com', 'teste', 'testando', 'password', capa
    )
    assert s_user is not None
    assert s_user.is_admin
    assert s_user.is_staff
    assert s_user.is_superuser
    assert s_user.nome == 'teste'
    assert s_user.sobrenome == 'testando'
    assert s_user.email == 'teste@teste.com'
    assert s_user.password != 'password'
    assert s_user.is_superuser
    assert s_user.delete()


@pytest.mark.django_db(transaction=True)
def test_user_without_email(capa):
    s_user = models.UserManager()
    with pytest.raises(ValueError):
        s_user = s_user.create_user(
            '', 'teste', 'testando', 'password', capa
        )


@pytest.mark.django_db(transaction=True)
def test_user_without_password(capa):
    s_user = models.UserManager()
    with pytest.raises(ValueError):
        s_user = s_user.create_user(
            'teste@teste.com', 'teste', 'testando', '', capa
        )


@pytest.mark.django_db(transaction=True)
def test_superuser_without_email(capa):
    s_user = models.UserManager()
    with pytest.raises(ValueError):
        s_user = s_user.create_superuser(
            '', 'teste', 'testando', 'password', capa
        )


@pytest.mark.django_db(transaction=True)
def test_superuser_without_password(capa):
    s_user = models.UserManager()
    with pytest.raises(ValueError):
        s_user = s_user.create_superuser(
            'teste@teste.com', 'teste', 'testando', '', capa
        )


@pytest.mark.django_db(transaction=True)
def test_user_pass_len_error(capa):
    s_user = models.UserManager()
    with pytest.raises(ValueError):
        s_user = s_user.create_user(
            'teste@teste.com', 'teste', 'testando', 'pass', capa
        )


@pytest.mark.django_db(transaction=True)
def test_supeuser_pass_len_error(capa):
    s_user = models.UserManager()
    with pytest.raises(ValueError):
        s_user = s_user.create_superuser(
            'teste@teste.com', 'teste', 'testando', 'pass', capa
        )


@pytest.mark.django_db(transaction=True)
def test_musica_type_wav(album, b64_arquivo_wav):
    with pytest.raises(ValueError):
        musica = models.Musica(
            nome='teste', album=album, ordem=1,
            arquivo=b64_arquivo_wav
        )
        musica.save()


@pytest.mark.django_db(transaction=True)
def test_musica_type_error(album, b64_arquivo_wav):
    with pytest.raises(ValueError):
        musica = models.Musica(
            nome='teste', album=album, ordem=1,
            arquivo=ContentFile(b64_arquivo_wav, 'teste.wav')
        )
        musica.save()


@pytest.mark.django_db(transaction=True)
def test_musica_file_invalid(album, capa):
    musica = models.Musica(
        nome='teste', album=album, ordem=1,
        arquivo=capa
    )
    with pytest.raises(ValueError):
        musica.save()


def test_repr_genero():
    assert repr(models.Genero()) == 'Genero()'


@pytest.mark.django_db(transaction=True)
def test_str_genero(genero):
    assert str(genero) == genero.descricao


def test_repr_banda():
    assert repr(models.Banda()) == 'Banda()'


@pytest.mark.django_db(transaction=True)
def test_str_banda(banda):
    assert str(banda) == banda.nome


def test_repr_album():
    assert repr(models.Album()) == 'Album()'


@pytest.mark.django_db(transaction=True)
def test_str_album(album):
    assert str(album) == album.nome


def test_repr_musica():
    assert repr(models.Musica()) == 'Musica()'


@pytest.mark.django_db(transaction=True)
def test_str_musica(musica):
    assert str(musica) == musica.nome


@pytest.mark.django_db(transaction=True)
def test_repr_like(like):
    assert repr(like) == f'Like({like.usuario.id}, {like.musica.id})'


@pytest.mark.django_db(transaction=True)
def test_str_like(like):
    assert str(like) == f'{like.usuario.id}, {like.musica.id}'
