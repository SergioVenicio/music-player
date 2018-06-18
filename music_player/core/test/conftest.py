import os
import pytest
import base64
from shutil import rmtree
from datetime import datetime
from music_player import settings
from music_player.core import models
from rest_framework.test import APIClient
from django.core.files.base import ContentFile
from music_player.core.utils import decode_file


@pytest.fixture
def usuario(request):
    usuario = models.Usuario(
        nome='teste', sobrenome='testando', email='teste@teste.com',
        password='password'
    )
    usuario.save()
    return usuario


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
def b64_capa_jpg(path):
    capa = open(path + '/imagem_test.png', 'rb').read()
    b64_capa = 'data:image/jpeg;base64,' + str(base64.b64encode(capa))[1:]
    print(b64_capa[11:15])
    return b64_capa


@pytest.fixture
def b64_capa_error(path):
    capa = open(path + '/imagem_test.png', 'rb').read()
    b64_capa = 'data:image/error;base64,' + str(base64.b64encode(capa))
    return b64_capa


@pytest.fixture
def arquivo(path):
    arquivo = open(path + '/musica_test.mp3', 'rb').read()
    b64_arquivo = base64.b64encode(arquivo)
    return ContentFile(decode_file(b64_arquivo), 'teste.mp3')


@pytest.fixture
def b64_arquivo(path):
    arquivo = open(path + '/musica_test.mp3', 'rb').read()
    header = 'data:audio/mpeg;base64,'
    b64_arquivo = str(base64.b64encode(arquivo))
    return header + b64_arquivo[1:]


@pytest.fixture
def b64_arquivo_wav(path):
    arquivo = open(path + '/musica_test.mp3', 'rb').read()
    header = 'data:audio/wav;base64,'
    b64_arquivo = str(base64.b64encode(arquivo))
    return header + b64_arquivo[1:]


@pytest.fixture
def genero(capa):
    genero = models.Genero(descricao='teste', imagem=capa)
    genero.save()
    yield genero
    img_dir = os.path.join(
        settings.BASE_DIR, settings.MEDIA_ROOT, genero.imagem.path
    )
    try:
        os.remove(img_dir)
    except FileNotFoundError:
        pass


@pytest.fixture
def banda(genero, capa):
    banda = models.Banda(
        nome='teste', imagem=capa, genero=genero
    )
    banda.save()
    yield banda
    img_dir = os.path.join(
        settings.BASE_DIR, settings.MEDIA_ROOT, banda.imagem.path
    )
    try:
        os.remove(img_dir)
    except FileNotFoundError:
        pass


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
    yield album
    img_dir = os.path.join(
        settings.BASE_DIR, settings.MEDIA_ROOT, album.capa.path
    )
    try:
        os.remove(img_dir)
    except FileNotFoundError:
        pass


@pytest.fixture
def musica(album, arquivo):
    musica = models.Musica(
        nome='teste', album=album, ordem=1, arquivo=arquivo
    )
    musica.save()
    yield musica
    music_dir = os.path.join(
        settings.BASE_DIR, settings.MEDIA_ROOT, musica.arquivo.path
    )
    teste_dir = os.path.join(
        settings.BASE_DIR, settings.MEDIA_ROOT,
        'musics', musica.album.banda.nome
    )

    try:
        os.remove(music_dir)
    except FileNotFoundError:
        pass

    rmtree(teste_dir)


@pytest.fixture
def api_client(usuario):
    api_client = APIClient()
    api_client.force_authenticate(user=usuario)
    return api_client
