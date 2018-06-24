import pytest
from rest_framework import status
from django.urls import reverse, resolve


@pytest.mark.django_db(transaction=True)
def test_criacao_musica(musica):
    assert isinstance(musica.id, int)
    assert 'teste' == musica.nome
    assert 'audio/mpeg' == musica.arquivo_tipo
    assert musica.delete()


@pytest.mark.django_db(transaction=True)
def test_get_view_musica(api_client):
    url = reverse(resolve('/api/v1/musicas').url_name)
    response = api_client.get(url)
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_get_view_musica_id(musica, api_client):
    url = reverse(resolve('/api/v1/musicas').url_name)
    response = api_client.get(url + f'/{musica.id}')
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_post_view_musica(api_client, album, b64_arquivo):
    url = reverse(resolve('/api/v1/musicas').url_name)
    data = {
        'nome': 'teste', 'album': album.id, 'ordem': 1, 'arquivo': b64_arquivo
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db(transaction=True)
def test_post_view_musica_arquivo_error(api_client, album):
    url = reverse(resolve('/api/v1/musicas').url_name)
    data = {
        'nome': 'teste', 'album': album.id, 'ordem': 1
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db(transaction=True)
def test_post_view_musica_album_error(api_client, b64_arquivo):
    url = reverse(resolve('/api/v1/musicas').url_name)
    data = {'nome': 'teste', 'arquivo': b64_arquivo}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db(transaction=True)
def test_post_view_musica_ordem_error(api_client, album, b64_arquivo):
    url = reverse(resolve('/api/v1/musicas').url_name)
    data = {
        'nome': 'teste', 'album': album.id, 'arquivo': b64_arquivo
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db(transaction=True)
def test_post_view_musica_existe_error(api_client, album, b64_arquivo):
    url = reverse(resolve('/api/v1/musicas').url_name)
    data = {
        'nome': 'teste', 'album': album.id, 'ordem': 1, 'arquivo': b64_arquivo
    }
    api_client.post(url, data, format='json')
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
