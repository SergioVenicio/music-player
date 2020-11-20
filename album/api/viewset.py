import json

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from ..models import Album
from .serializer import AlbumSerializer


from shared.file.services.FileDecoder import FileDecoder
from shared.redis.RedisService import RedisService


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    http_method_names = ['get', 'post']

    cache = RedisService()

    def get_queryset(self):
        cache_key = 'albuns'

        band_id = self.request.query_params.get('band_id')
        if band_id:
            cache_key = f'albuns@{band_id}'

        data = self.cache.get(cache_key)
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
            print(data)
            self.cache.set(cache_key, data)

        return data

    def retrieve(self, request, pk=None, *args, **kwargs):
        cache_key = f'album@{pk}'
        cache_data = self.cache.get(cache_key)
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
        self.cache.set(
            cache_key,
            value=response_data
        )
        return Response(data=response_data)

    def create(self, request, *args, **kwargs):
        file_decoder = FileDecoder()
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
        self.cache.set(
            f'album@{album.id}',
            album.to_dict()
        )

        response = json.dumps({
            'album': {
                'id': album.id,
                'name': album.name,
                'band_id': album.band.id,
                'release_date': album.release_date,
                'cover_image': album.cover_image.path
            }
        })
        return Response(response, status=201)
