import pytest
from rest_framework import status
from django.urls import reverse, resolve


@pytest.mark.django_db(transaction=True)
def test_criacao_musica(musica):
    assert isinstance(musica.id, int)
    assert 'teste' == musica.nome
    assert 'audio/mpeg' == musica.arquivo_tipo


@pytest.mark.django_db(transaction=True)
def test_apaga_musica(musica):
    assert bool(musica.delete()) == True


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
