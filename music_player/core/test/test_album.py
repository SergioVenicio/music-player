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
