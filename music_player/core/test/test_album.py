import pytest
from rest_framework import status
from django.urls import reverse, resolve


@pytest.mark.django_db(transaction=True)
def test_criacao_album(album, ano):
    assert isinstance(album.id, int)
    assert 'teste' == album.nome
    assert album.data_lancamento == ano
    assert album.capa is not None
    assert album.delete()


@pytest.mark.django_db(transaction=True)
def test_get_view_album(api_client, usuario):
    url = reverse(resolve('/api/v1/album').url_name)
    response = api_client.get(url)
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_get_view_album_id(api_client, album):
    url = reverse(resolve('/api/v1/album').url_name)
    response = api_client.get(url + f'/{album.id}')
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_post_view_album(api_client, banda, ano, usuario):
    url = reverse(resolve('/api/v1/album').url_name)
    data = {'nome': 'teste', 'banda_id': banda.id, 'data_lancamento': ano}
    api_client.force_authenticate(user=usuario)
    response = api_client.post(url, data, format='json')
    assert status.is_success(response.status_code)
