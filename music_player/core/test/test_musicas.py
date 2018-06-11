import pytest
from rest_framework import status
from django.urls import reverse, resolve


@pytest.mark.django_db(transaction=True)
def test_criacao_musica(musica):
    assert isinstance(musica.id, int)
    assert 'teste' == musica.nome
    assert 'audio/mpeg' == musica.arquivo_tipo


@pytest.mark.django_db(transaction=True)
def test_get_view_musica(client):
    url = reverse(resolve('/api_v1/musicas').url_name)
    response = client.get(url)
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_get_view_musica_id(musica, client):
    url = reverse(resolve('/api_v1/musicas').url_name)
    response = client.get(url + f'/{musica.id}')
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_post_view_musica(api_client, album, b64_arquivo):
    url = reverse(resolve('/api_v1/musicas').url_name)
    data = {
        'nome': 'teste', 'album': album.id, 'ordem': 1, 'arquivo': b64_arquivo
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
