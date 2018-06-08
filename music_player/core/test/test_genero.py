import pytest
import base64
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
