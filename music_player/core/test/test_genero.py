import pytest
from core.models import Genero


@pytest.mark.django_db(transaction=True)
def test_criacao_genero():
    genero = Genero.objects.create(descricao='Teste')
    assert isinstance(genero.id, int)
    assert 'Teste' == genero.descricao
