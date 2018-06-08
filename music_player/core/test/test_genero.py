import pytest
import base64
from django.test import Client
from rest_framework import status
from django.urls import reverse, resolve
from rest_framework.test import APIClient
from music_player.core.models import Genero
from django.core.files.base import ContentFile
from music_player.core.utils import decode_file


@pytest.mark.django_db(transaction=True)
def test_criacao_genero():
    path = 'music_player/core/test'
    capa = open(path + '/imagem_test.png', 'rb').read()
    b64_capa = base64.b64encode(capa)
    capa = ContentFile(decode_file(b64_capa), 'teste.png')
    genero = Genero(descricao='Teste', imagen=capa)
    genero.save()
    assert isinstance(genero.id, int)
    assert 'Teste' == genero.descricao
    assert genero.imagen is not None


@pytest.mark.django_db(transaction=True)
def test_get_view_genero():
    client = Client()
    url = reverse(resolve('/api_v1/genero').url_name)
    response = client.get(url)
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_post_view_genero():
    client = APIClient()
    url = reverse(resolve('/api_v1/genero').url_name)
    path = 'music_player/core/test'
    capa = open(path + '/imagem_test.png', 'rb').read()
    b64_capa = 'data:image/png;base64,' + str(base64.b64encode(capa))
    data = {'descricao': 'teste', 'imagen': b64_capa}
    response = client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
