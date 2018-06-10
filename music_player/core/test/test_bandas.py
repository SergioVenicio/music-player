import pytest
from django.test import Client
from rest_framework import status
from django.urls import reverse, resolve


@pytest.mark.django_db(transaction=True)
def test_criacao_banda(banda):
    assert isinstance(banda.id, int)
    assert 'teste' == banda.nome
    assert banda.imagem is not None


@pytest.mark.django_db(transaction=True)
def test_get_view_banda():
    client = Client()
    url = reverse(resolve('/api_v1/banda').url_name)
    response = client.get(url)
    assert status.is_success(response.status_code)
