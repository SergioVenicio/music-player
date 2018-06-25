import random
import pytest
from rest_framework import status
from django.urls import reverse, resolve


@pytest.mark.django_db(transaction=True)
def test_criacao_likes(like):
    assert isinstance(like.id, int)
    assert isinstance(like.usuario.id, int)
    assert isinstance(like.musica.id, int)
    assert like.delete()


@pytest.mark.django_db(transaction=True)
def test_get_view_like(api_client, like):
    url = reverse(resolve('/api/v1/likes').url_name)
    response = api_client.get(url)
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_get_view_like_usuario(api_client, like):
    usuario_id = like.usuario.id
    url = reverse(
        resolve('/api/v1/likes').url_name
    )
    response = api_client.get(url + f'/usuario/{usuario_id}')
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_get_view_like_usuario_not_found(api_client, like):
    usuario_id = like.usuario.id + random.randint(100, 1000)
    url = reverse(
        resolve('/api/v1/likes').url_name
    )
    response = api_client.get(url + f'/usuario/{usuario_id}')
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_get_view_like_usuario_error(api_client, like):
    usuario_id = 'b'
    url = reverse(
        resolve('/api/v1/likes').url_name
    )
    response = api_client.get(url + f'/usuario/{usuario_id}')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db(transaction=True)
def test_get_view_like_musica(api_client, like):
    usuario_id = like.usuario.id
    musica_id = like.musica.id
    url = reverse(resolve('/api/v1/likes').url_name)
    response = api_client.get(url + f'/usuario/{usuario_id}/{musica_id}')
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_get_view_like_musica_not_found(api_client, like):
    usuario_id = like.usuario.id
    musica_id = like.musica.id + random.randint(100, 1000)
    url = reverse(resolve('/api/v1/likes').url_name)
    response = api_client.get(url + f'/usuario/{usuario_id}/{musica_id}')
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_get_view_like_musica_error(api_client, like):
    usuario_id = like.usuario.id
    musica_id = 'b'
    url = reverse(resolve('/api/v1/likes').url_name)
    response = api_client.get(url + f'/usuario/{usuario_id}/{musica_id}')
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db(transaction=True)
def create_like(api_client, usuario, musica):
    url = reverse(resolve('/api/v1/likes').url_name)
    data = {'usuario': usuario.id, 'musica': musica.id}
    reponse = api_client.post(url, data, format='json')
    assert reponse.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db(transaction=True)
def test_create_like_error(api_client):
    url = reverse(resolve('/api/v1/likes').url_name)
    data = {}
    reponse = api_client.post(url, data, format='json')
    assert reponse.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db(transaction=True)
def test_create_like_existe(api_client, usuario, musica):
    url = reverse(resolve('/api/v1/likes').url_name)
    data = {'usuario': usuario.id, 'musica': musica.id}
    reponse_1 = api_client.post(url, data, format='json')
    reponse_2 = api_client.post(url, data, format='json')
    assert reponse_1.status_code == status.HTTP_201_CREATED
    assert reponse_2.status_code == status.HTTP_201_CREATED
