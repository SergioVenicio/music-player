import pytest
from rest_framework import status
from django.urls import reverse, resolve


@pytest.mark.django_db(transaction=True)
def test_criacao_album(album, ano):
    assert isinstance(album.id, int)
    assert 'teste' == album.nome
    assert album.data_lancamento == ano
    assert album.capa is not None


@pytest.mark.django_db(transaction=True)
def test_get_view_album(client):
    url = reverse(resolve('/api_v1/album').url_name)
    response = client.get(url)
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_get_view_album_id(client, album):
    url = reverse(resolve('/api_v1/album').url_name)
    response = client.get(url + f'/{album.id}')
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_post_view_album(api_client, banda, ano):
    url = reverse(resolve('/api_v1/album').url_name)
    data = {'nome': 'teste', 'banda_id': banda.id, 'data_lancamento': ano}
    response = api_client.post(url, data, format='json')
    assert status.is_success(response.status_code)
