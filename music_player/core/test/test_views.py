import pytest
from rest_framework import status
from music_player.core import models
from django.urls import reverse, resolve


@pytest.mark.django_db(transaction=True)
def test_home(client):
    user = models.Usuario(
        nome='teste', sobrenome='testando',
        email='teste@testando.com.br',
        password='password'
    )
    user.save()
    client.force_login(user)
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db(transaction=True)
def test_home_redirect(client):
    response = client.get('/')
    assert response.status_code == status.HTTP_302_FOUND


@pytest.mark.django_db(transaction=True)
def test_user_avatar_get(client):
    user = models.Usuario(
        nome='teste', sobrenome='testando',
        email='teste@testando.com.br',
        password='password'
    )
    user.save()
    url = '/avatar/'
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db(transaction=True)
def test_user_avatar_redirect(client):
    url = '/avatar/'
    response = client.get(url)
    assert response.status_code == status.HTTP_302_FOUND


@pytest.mark.django_db(transaction=True)
def test_bandas_get(client, banda):
        user = models.Usuario(
            nome='teste', sobrenome='testando',
            email='teste@testando.com.br',
            password='password'
        )
        user.save()
        url = '/bandas'
        client.force_login(user)
        response = client.get(f'{url}/{banda.id}')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db(transaction=True)
def test_bandas_redirect(client, banda):
        url = '/bandas'
        response = client.get(f'{url}/{banda.id}')
        assert response.status_code == status.HTTP_302_FOUND


@pytest.mark.django_db(transaction=True)
def test_bandas_add_get(client, banda):
        user = models.Usuario(
            nome='teste', sobrenome='testando',
            email='teste@testando.com.br',
            password='password'
        )
        user.save()
        url = reverse(resolve('/bandas/add').url_name)
        client.force_login(user)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db(transaction=True)
def test_albuns_get(client, album):
        user = models.Usuario(
            nome='teste', sobrenome='testando',
            email='teste@testando.com.br',
            password='password'
        )
        user.save()
        url = '/albuns'
        client.force_login(user)
        response = client.get(f'{url}/{album.id}')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db(transaction=True)
def test_albuns_redirect(client, album):
        url = '/albuns'
        response = client.get(f'{url}/{album.id}')
        assert response.status_code == status.HTTP_302_FOUND


@pytest.mark.django_db(transaction=True)
def test_albuns_add_get(client, album):
        user = models.Usuario(
            nome='teste', sobrenome='testando',
            email='teste@testando.com.br',
            password='password'
        )
        user.save()
        url = '/albuns/add'
        client.force_login(user)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db(transaction=True)
def test_albuns_add_redirect(client, album):
        url = '/albuns/add'
        response = client.get(url)
        assert response.status_code == status.HTTP_302_FOUND


@pytest.mark.django_db(transaction=True)
def test_bandas_add_redirect(client, banda):
        url = reverse(resolve('/bandas/add').url_name)
        response = client.get(url)
        assert response.status_code == status.HTTP_302_FOUND


@pytest.mark.django_db(transaction=True)
def test_musicas_get(client, album):
        user = models.Usuario(
            nome='teste', sobrenome='testando',
            email='teste@testando.com.br',
            password='password'
        )
        user.save()
        url = '/musicas'
        client.force_login(user)
        response = client.get(f'{url}/{album.id}')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db(transaction=True)
def test_musicas_get_redirect(client, musica):
        url = '/musicas'
        response = client.get(f'{url}/{musica.id}')
        assert response.status_code == status.HTTP_302_FOUND


@pytest.mark.django_db(transaction=True)
def test_musica_add_get(client):
        user = models.Usuario(
            nome='teste', sobrenome='testando',
            email='teste@testando.com.br',
            password='password'
        )
        user.save()
        url = '/musicas/add'
        client.force_login(user)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db(transaction=True)
def test_favoritas_get(client):
        user = models.Usuario(
            nome='teste', sobrenome='testando',
            email='teste@testando.com.br',
            password='password'
        )
        user.save()
        url = '/favoritas'
        client.force_login(user)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db(transaction=True)
def test_musica_add_get_redirect(client):
        url = '/musicas/add'
        response = client.get(url)
        assert response.status_code == status.HTTP_302_FOUND


@pytest.mark.django_db(transaction=True)
def test_genero_get(client):
        user = models.Usuario(
            nome='teste', sobrenome='testando',
            email='teste@testando.com.br',
            password='password'
        )
        user.save()
        url = '/generos/add'
        client.force_login(user)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db(transaction=True)
def test_genero_get_redirect(client):
        url = '/generos/add'
        response = client.get(url)
        assert response.status_code == status.HTTP_302_FOUND


@pytest.mark.django_db(transaction=True)
def test_singup_get(client):
    response = client.post(reverse(resolve('/sign_up').url_name))
    assert response.status_code == status.HTTP_200_OK
