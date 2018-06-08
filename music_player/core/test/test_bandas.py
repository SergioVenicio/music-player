import pytest
import base64
from django.test import Client
from rest_framework import status
from music_player.core import models
from django.urls import reverse, resolve
from django.core.files.base import ContentFile
from music_player.core.utils import decode_file


@pytest.mark.django_db(transaction=True)
def test_criacao_banda():
    genero = models.Genero(descricao='Teste')
    genero.save()

    path = 'music_player/core/test'
    capa = open(path + '/imagem_test.png', 'rb').read()
    b64_capa = base64.b64encode(capa)
    capa = ContentFile(decode_file(b64_capa), 'teste.png')

    banda = models.Banda(nome='Teste', imagen=capa, genero=genero)
    banda.save()

    assert isinstance(banda.id, int)
    assert 'Teste' == banda.nome
    assert banda.imagen is not None


@pytest.mark.django_db(transaction=True)
def test_get_view_banda():
    client = Client()
    url = reverse(resolve('/api_v1/banda').url_name)
    response = client.get(url)
    assert status.is_success(response.status_code)
