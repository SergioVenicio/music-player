import pytest

from rest_framework import status

from band.models import Band, Genre
from album import models

from tests.baseTests.base_test import BaseTest, HttpBaseClass


class AlbumBaseTest(BaseTest):
    def setUp(self):
        super().setUp()

        self.genre = Genre(
            description='test',
            genre_image=self._get_image()
        )
        self.band = Band(
            name='test',
            genre=self.genre,
            band_image=self._get_image()
        )

        self.genre.save()
        self.band.save()

    def tearDown(self):
        self.band.delete()
        self.genre.delete()

        super().tearDown()

    def get_new_album(self):
        album = models.Album(
            name='test',
            band=self.band,
            release_date=2020,
            cover_image=self._get_image(),
        )

        album.save()
        return album


@pytest.mark.django_db(transaction=True)
class TestAlbum(AlbumBaseTest):
    def test_create(self):
        album = self.get_new_album()

        assert album.id is not None
        assert album.name == 'test'

    def test_update(self):
        album = self.get_new_album()

        album.name = 'New name'
        album.save()

        assert album.name == 'New name'

    def test_delete(self):
        album = self.get_new_album()

        album_id = album.id
        album.delete()

        assert album_id not in models.Album.objects.all().values('id')


@pytest.mark.django_db(transaction=True)
class TestAlbumView(AlbumBaseTest, HttpBaseClass):
    def setUp(self):
        AlbumBaseTest.setUp(self)
        HttpBaseClass.setUp(self)

        self.url = self.get_url('/api/v1/album')

    def test_request_get(self):
        self.get_new_album()
        response = self.api_client.get(self.url)

        assert status.is_success(response.status_code)
        assert response.json()['results'][0].get('cover_image') is not None

    def test_request_post(self):
        cover_image = self._get_raw_image()

        data = {
            'name': 'test_request',
            'band_id': self.band.id,
            'release_date': 2020,
            'cover_image': cover_image
        }
        response = self.api_client.post(
            self.url,
            data,
            format='json'
        )

        assert response.status_code == 201

    def test_request_post_with_invalid_relea_date(self):
        cover_image = self._get_raw_image()

        data = {
            'name': 'test_request',
            'band_id': self.band.id,
            'release_date': 'fff',
            'cover_image': cover_image
        }
        response = self.api_client.post(
            self.url,
            data,
            format='json'
        )

        assert response.status_code == 400

    def test_request_post_with_anonymous_user(self):
        cover_image = self._get_raw_image()

        data = {
            'name': 'test_request',
            'band_id': self.band.id,
            'release_date': 2020,
            'cover_image': cover_image
        }
        response = self.anonymous_client.post(
            self.url,
            data,
            format='json'
        )

        assert response.status_code == 401
