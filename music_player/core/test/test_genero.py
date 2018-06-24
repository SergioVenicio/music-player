import pytest
from rest_framework import status
from django.urls import reverse, resolve


@pytest.mark.django_db(transaction=True)
def test_criacao_genero(genero):
    assert isinstance(genero.id, int)
    assert 'teste' == genero.descricao
    assert genero.imagem is not None


@pytest.mark.django_db(transaction=True)
def test_apaga_genero(genero):
    assert bool(genero.delete())


@pytest.mark.django_db(transaction=True)
def test_get_view_genero(api_client):
    url = reverse(resolve('/api/v1/genero').url_name)
    response = api_client.get(url)
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_get_view_genero_id(api_client, genero):
    url = reverse(resolve('/api/v1/genero').url_name)
    response = api_client.get(url + f'/{genero.id}')
    assert status.is_success(response.status_code)


@pytest.mark.django_db(transaction=True)
def test_get_view_home_genero_without_login(client, genero):
    url = ''
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db(transaction=True)
def test_post_view_genero(api_client):
    url = reverse(resolve('/api/v1/genero').url_name)
    data = {'descricao': 'teste'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db(transaction=True)
def test_post_view_genero_desc_error(api_client):
    url = reverse(resolve('/api/v1/genero').url_name)
    data = {'descricao': 'teste'}
    response = api_client.post(url, data, format='json')
    data = {'descricao': 'teste'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db(transaction=True)
def test_post_view_genero_imagem(b64_capa, api_client):
    url = reverse(resolve('/api/v1/genero').url_name)
    data = {'descricao': 'teste', 'imagem': b64_capa}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db(transaction=True)
def test_post_view_genero_imagem_jpeg(b64_capa_jpeg, api_client):
    url = reverse(resolve('/api/v1/genero').url_name)
    data = {'descricao': 'teste', 'imagem': b64_capa_jpeg}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db(transaction=True)
def test_post_view_genero_imagem_error(b64_capa_error, api_client):
    url = reverse(resolve('/api/v1/genero').url_name)
    data = {'descricao': 'teste', 'imagem': b64_capa_error}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
