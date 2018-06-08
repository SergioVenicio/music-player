import pytest
import base64
from datetime import datetime
from django.test import Client
from rest_framework import status
from music_player.core import models
from django.urls import reverse, resolve
from django.core.files.base import ContentFile
from music_player.core.utils import decode_file


@pytest.mark.django_db(transaction=True)
def test_criacao_musica():
    path = 'music_player/core/test'

    arquivo = open(path + '/musica_test.mp3', 'rb').read()
    b64_arquivo = base64.b64encode(arquivo)

    capa = open(path + '/imagem_test.png', 'rb').read()
    b64_capa = base64.b64encode(capa)

    capa = ContentFile(decode_file(b64_capa), 'teste.png')
    arquivo = ContentFile(decode_file(b64_arquivo), 'teste.mp3')

    genero = models.Genero(descricao='Teste')
    genero.save()

    banda = models.Banda(
        nome='teste', imagen=capa, genero=genero
    )
    banda.save()

    album = models.Album(
        nome='teste', banda=banda,
        data_lancamento=datetime.now().year, capa=capa
    )
    album.save()

    musica = models.Musica(
        nome='teste', album=album, ordem=1, arquivo=arquivo
    )
    musica.save()
    assert isinstance(musica.id, int)
    assert 'teste' == musica.nome
    assert 'audio/mpeg' == musica.arquivo_tipo


@pytest.mark.django_db(transaction=True)
def test_get_view_musica():
    client = Client()
    url = reverse(resolve('/api_v1/musicas').url_name)
    response = client.get(url)
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_get_view_musica_id():
    path = 'music_player/core/test'

    arquivo = open(path + '/musica_test.mp3', 'rb').read()
    b64_arquivo = base64.b64encode(arquivo)

    capa = open(path + '/imagem_test.png', 'rb').read()
    b64_capa = base64.b64encode(capa)

    capa = ContentFile(decode_file(b64_capa), 'teste.png')
    arquivo = ContentFile(decode_file(b64_arquivo), 'teste.mp3')

    genero = models.Genero(descricao='Teste')
    genero.save()

    banda = models.Banda(
        nome='teste', imagen=capa, genero=genero
    )
    banda.save()

    album = models.Album(
        nome='teste', banda=banda,
        data_lancamento=datetime.now().year, capa=capa
    )
    album.save()

    musica = models.Musica(
        nome='teste', album=album, ordem=1, arquivo=arquivo
    )
    musica.save()
    id = musica.id
    client = Client()
    url = reverse(resolve('/api_v1/musicas').url_name)
    response = client.get(url + f'/{id}')
    assert status.is_success(response.status_code)
