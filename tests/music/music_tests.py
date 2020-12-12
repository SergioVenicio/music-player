import pytest

from rest_framework import status

from album.models import Album
from music.models import Music
from band.models import Band, Genre

from tests.baseTests.base_test import BaseTest, HttpBaseClass


class MusicBaseTest(BaseTest):
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

        self.album = Album(
            name='test',
            band=self.band,
            release_date=2020,
            cover_image=self._get_image()
        )

        self.genre.save()
        self.band.save()
        self.album.save()

    def tearDown(self):
        self.genre.delete()
        self.band.delete()

        super().tearDown()

    def get_new_music(self):
        music = Music(
            name='Test',
            album=self.album,
            order=1,
            file=self._get_mp3()
        )

        music.save()
        return music


@pytest.mark.django_db(transaction=True)
class TestMusic(MusicBaseTest):
    def test_create(self):
        music = self.get_new_music()

        assert music.id is not None
        assert music.name == 'Test'
        assert str(music.duration) != ''
        assert music.file_type == 'audio/mpeg'

    def test_delete(self):
        music = self.get_new_music()

        music_id = music.id
        music.delete()

        assert music_id not in Music.objects.all().values('id')


@pytest.mark.django_db(transaction=True)
class TestMusicView(MusicBaseTest, HttpBaseClass):
    def setUp(self):
        MusicBaseTest.setUp(self)
        HttpBaseClass.setUp(self)

        self.url = self.get_url('/api/v1/music')

    def test_request_get(self):
        self.get_new_music()
        response = self.api_client.get(self.url)

        assert status.is_success(response.status_code)
        assert len(response.json()['results']) >= 1

    def test_request_get_by_id(self):
        music = self.get_new_music()
        url = self.get_reverse_url('music-detail', pk=music.id)
        response = self.api_client.get(url)

        assert status.is_success(response.status_code)

    def test_request_post(self):
        data = {
            'name': 'test_request.mp3',
            'album_id': self.album.id,
            'order': 1,
            'file': self._get_raw_mp3()
        }
        response = self.api_client.post(
            self.url,
            data,
            format='json'
        )

        assert response.status_code == 201

    def test_request_post_with_a_repeated_order(self):
        data = {
            'name': 'test_request.mp3',
            'album_id': self.album.id,
            'order': 1,
            'file': self._get_raw_mp3()
        }
        response = self.api_client.post(
            self.url,
            data,
            format='json'
        )

        response = self.api_client.post(
            self.url,
            data,
            format='json'
        )

        assert response.status_code == 400

    def test_request_post_with_a_invalid_file(self):
        data = {
            'name': 'test_request.jpeg',
            'album_id': self.album.id,
            'order': 1,
            'file': self._get_raw_image()
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
            'album_id': self.album.id,
            'order': 1,
            'file': self._get_raw_mp3()
        }
        response = self.anonymous_client.post(
            self.url,
            data,
            format='json'
        )

        assert response.status_code == 401
