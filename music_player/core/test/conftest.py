import pytest
import base64
from datetime import datetime
from django.test import Client
from music_player.core import models
from rest_framework.test import APIClient
from django.core.files.base import ContentFile
from music_player.core.utils import decode_file


@pytest.fixture
def path():
    return 'music_player/core/test'


@pytest.fixture
def capa(path):
    capa = open(path + '/imagem_test.png', 'rb').read()
    b64_capa = base64.b64encode(capa)
    return ContentFile(decode_file(b64_capa), 'teste.png')


@pytest.fixture
def b64_capa(path):
    capa = open(path + '/imagem_test.png', 'rb').read()
    b64_capa = 'data:image/png;base64,' + str(base64.b64encode(capa))
    return b64_capa


@pytest.fixture
def arquivo(path):
    arquivo = open(path + '/musica_test.mp3', 'rb').read()
    b64_arquivo = base64.b64encode(arquivo)
    return ContentFile(decode_file(b64_arquivo), 'teste.mp3')


@pytest.fixture
def genero():
    genero = models.Genero(descricao='teste')
    genero.save()
    return genero


@pytest.fixture
def banda(genero, capa):
    banda = models.Banda(
        nome='teste', imagem=capa, genero=genero
    )
    banda.save()
    return banda


@pytest.fixture
def ano():
    return datetime.now().year


@pytest.fixture
def album(banda, capa, ano):
    album = models.Album(
        nome='teste', banda=banda,
        data_lancamento=ano, capa=capa
    )
    album.save()
    return album


@pytest.fixture
def musica(album, arquivo):
    musica = models.Musica(
        nome='teste', album=album, ordem=1, arquivo=arquivo
    )
    musica.save()
    return musica


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def api_client():
    return APIClient()
