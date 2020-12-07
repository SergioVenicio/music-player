import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from ..models import Album
from .serializer import AlbumSerializer

from dependency_injector.wiring import inject, Provide

from music_player.containers import Container
from shared.cache.services import ABCCacheService
from shared.file.services.FileDecoder import ABCFileDecoder


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    http_method_names = ['get', 'post']

    @inject
    def get_queryset(
        self,
        cache: ABCCacheService = Provide[Container.cache_service]
    ):
        cache_key = 'albuns'

        band_id = self.request.query_params.get('band_id')
        if band_id:
            cache_key = f'albuns:band_id@{band_id}'

        cache.unset(cache_key)
        data = cache.get(cache_key)
        if not data:
            queryset = self.queryset
            if band_id:
                queryset = queryset.filter(
                    band_id=band_id
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
        cache_data = cache.get(cache_key)
        if cache_data:
            return Response(cache_data)

        def filter_id(album: dict):
            album_id = album.get(('id'))
            return album_id is not None and str(album_id) == str(pk)

        db_data = list(filter(filter_id, self.get_queryset()))
        if not db_data:
            return Response(data={}, status=404)

        serializer = self.serializer_class(
            db_data[0],
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
        band_id = request.data.get('band_id', None)

        if not band_id:
            return Response(
                data={
                    'status': 'error',
                    'error': 'band_id field is required!'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        release_date = request.data.get('release_date', None)
        cover_image_raw = request.data.get('cover_image', None)

        try:
            cover_image = file_decoder.execute(
                cover_image_raw,
                name
            )
        except ValueError:
            return Response(
                data={
                    'status': 'error',
                    'error': 'invalid image type!'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        album = Album(
            name=name,
            band_id=band_id,
            release_date=release_date,
            cover_image=cover_image
        )
        album.save()

        response = json.dumps({
            'album': {
                'id': album.id,
                'name': album.name,
                'band_id': album.band.id,
                'release_date': album.release_date,
                'cover_image': album.cover_image.path
            }
        })
        return Response(data=response, status=201)
