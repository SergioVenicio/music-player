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
    url = reverse(resolve('/api/v1/banda').url_name)
    response = client.get(url)
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_get_view_banda_id(banda):
    client = Client()
    url = reverse(resolve('/api/v1/banda').url_name)
    response = client.get(url + f'/{banda.id}')
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_post_view_banda(api_client, genero):
    url = reverse(resolve('/api/v1/banda').url_name)
    data = {'nome': 'teste', 'genero_id': genero.id}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db(transaction=True)
def test_post_view_banda_img(api_client, genero, b64_capa):
    url = reverse(resolve('/api/v1/banda').url_name)
    data = {'nome': 'teste', 'genero_id': genero.id, 'imagem': b64_capa}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
