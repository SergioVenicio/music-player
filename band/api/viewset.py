
import json

from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from ..models import Band, Genre
from .serializer import BandSerializer, GenreSerializer

from dependency_injector.wiring import inject, Provide
from music_player.containers import Container
from shared.cache.services import ABCCacheService
from shared.file.services.FileDecoder import ABCFileDecoder


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    http_method_names = ['get', 'post']

    @inject
    def get_queryset(
        self,
        cache: ABCCacheService = Provide[Container.cache_service]
    ):
        cache_key = 'genres'
        data = cache.get(cache_key)

        if not data:
            data = [
                album.to_dict()
                for album in self.queryset.all()
            ]
            cache.set(cache_key, data)

        return data

    def create(
        self,
        request,
        file_decoder: ABCFileDecoder = Provide[Container.file_decoder_service]
    ):
        description = request.data['description']
        genre_image_raw = request.data['genre_image']

        if not genre_image_raw:
            return Response(data={
                'status': 'error',
                'error': 'Genre image field is required!'
            }, status=400)

        try:
            decoded_image = file_decoder.execute(genre_image_raw, description)
        except ValueError:
            return Response(data={
                'status': 'error',
                'error': 'Invalid file type!'
            }, status=400)

        genre = Genre(description=description, genre_image=decoded_image)
        try:
            genre.save()
            return Response(data=json.dumps({
                'genre': {
                    'id': genre.id,
                    'description': genre.description,
                    'genre_image': genre.genre_image.path
                }
            }), status=201)
        except IntegrityError:
            return Response(data={
                'status': 'error',
                'error': 'Invalid genre description!'
            }, status=400)


class BandViewSet(viewsets.ModelViewSet):
    queryset = Band.objects.all()
    serializer_class = BandSerializer
    http_method_names = ['get', 'post']

    @inject
    def get_queryset(
        self,
        cache: ABCCacheService = Provide[Container.cache_service]
    ):
        cache_key = 'bands'
        genre_id = self.request.query_params.get('genre_id')

        if genre_id:
            cache_key = f'bands:genre_id@{genre_id}'

        data = cache.get(cache_key)
        if not data:
            queryset = self.queryset
            if genre_id:
                queryset = queryset.filter(
                    genre_id=genre_id
                )
            data = [
                album.to_dict()
                for album in queryset.all()
            ]
            cache.set(cache_key, data)

        return data

    @inject
    def retrieve(
        self,
        request,
        pk=None,
        cache: ABCCacheService = Provide[Container.cache_service]
    ):
        cache_key = f'album@{pk}'
        cache.unset(cache_key)
        cache_data = cache.get(cache_key)
        if cache_data:
            return Response(cache_data)

        db_data = get_object_or_404(
            self.get_queryset(),
            pk=pk
        )

        serializer = self.serializer_class(
            db_data,
            context={'request': request}
        )
        response_data = serializer.data
        cache.set(
            cache_key,
            value=response_data
        )
        return Response(data=response_data)

    @inject
    def create(
        self,
        request,
        file_decoder: ABCFileDecoder = Provide[Container.file_decoder_service]
    ):
        name = request.data.get('name', None)
        genre_id = request.data.get('genre_id', None)
        band_image_raw = request.data.get('band_image', None)

        if not name:
            return Response(data={
                'status': 'error',
                'error': 'Band name fild is required!'
            }, status=400)

        if not genre_id:
            return Response(data={
                'status': 'error',
                'error': 'Genre id fild is required!'
            }, status=400)

        if not band_image_raw:
            return Response(data={
                'status': 'error',
                'error': 'Band image fild is required!'
            }, status=400)

        try:
            band_image = file_decoder.execute(band_image_raw, name)
        except ValueError:
            return Response(data={
                'status': 'error',
                'error': 'Invalid image type!'
            }, status=400)

        band = Band(
            name=name,
            genre_id=genre_id,
            band_image=band_image
        )
        try:
            band.save()
        except IntegrityError:
            return Response(data={
                'status': 'error',
                'error': 'This band already exists!'
            }, status=400)

        return Response(data={
            'band': {
                'id': band.id,
                'name': band.name,
                'band_image': band.band_image.path
            }
        }, status=201)
