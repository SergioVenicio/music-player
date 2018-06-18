import pytest
from music_player.core import models


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
