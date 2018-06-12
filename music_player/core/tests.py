from rest_framework import status
from django.urls import reverse, resolve
from rest_framework.test import APITestCase


class TestBandas(APITestCase):
    url = reverse(resolve('/api/v1/banda').url_name)

    def test_list_bandas(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestGeneros(APITestCase):
    url = reverse(resolve('/api/v1/genero').url_name)

    def test_list_generos(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestAlbum(APITestCase):
    url = reverse(resolve('/api/v1/album').url_name)

    def test_list_albuns(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestMusicas(APITestCase):
    url = reverse(resolve('/api/v1/musicas').url_name)

    def test_list_albuns(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
