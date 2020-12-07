import pytest

from rest_framework import status

from band.models import Band, Genre

from tests.baseTests.base_test import BaseTest, HttpBaseClass


class BandBaseTest(BaseTest):
    def setUp(self):
        super().setUp()

        self.genre = Genre(
            description='test',
            genre_image=self._get_image()
        )

        self.genre.save()

    def tearDown(self):
        self.genre.delete()

        super().tearDown()

    def get_new_band(self):
        band = Band(
            name='Test',
            genre=self.genre,
            band_image=self._get_image()
        )
        band.save()
        return band


@pytest.mark.django_db(transaction=True)
class TestBand(BandBaseTest):
    def test_create(self):
        band = self.get_new_band()

        assert band.id is not None
        assert band.name == 'Test'

    def test_delete(self):
        band = self.get_new_band()

        band_id = band.id
        band.delete()

        assert band_id not in Band.objects.all().values('id')


@pytest.mark.django_db(transaction=True)
class TestBandView(BandBaseTest, HttpBaseClass):
    def setUp(self):
        BandBaseTest.setUp(self)
        HttpBaseClass.setUp(self)

        self.url = self.get_url('/api/v1/band')

    def test_request_get(self):
        self.get_new_band()
        response = self.api_client.get(self.url)

        assert status.is_success(response.status_code)
        assert len(response.json()['results']) >= 1

    def test_request_post(self):
        data = {
            'name': 'test_request',
            'genre_id': self.genre.id,
            'band_image': self._get_raw_image()
        }
        response = self.api_client.post(
            self.url,
            data,
            format='json'
        )

        assert response.status_code == 201

    def test_request_with_invalid_genre(self):
        data = {
            'name': 'test_request',
            'genre_id': self.genre.id + 122,
            'band_image': self._get_raw_image()
        }
        response = self.api_client.post(
            self.url,
            data,
            format='json'
        )

        assert response.status_code == 400

    def test_request_post_with_anonymous_user(self):
        data = {
            'name': 'test_request',
            'genre_id': self.genre.id,
            'band_image': self._get_raw_image()
        }
        response = self.anonymous_client.post(
            self.url,
            data,
            format='json'
        )

        assert response.status_code == 401
