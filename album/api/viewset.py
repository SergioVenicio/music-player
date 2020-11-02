import json

from rest_framework import status
from rest_framework.response import Response
from django.core.files.base import ContentFile
from rest_framework import viewsets

from ..models import Album
from .serializer import AlbumSerializer

from music_player.core.utils import get_file_type, decode_file


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all().order_by('release_date')
    serializer_class = AlbumSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
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
        cover_image = request.data.get('cover_image', None)

        type_ = get_file_type(cover_image)
        if type_ == '.jpg':
            cover_image = cover_image[23:]
        elif type_ == '.png':
            cover_image = cover_image[22:]
        else:
            return Response(
                data={
                    'status': 'error',
                    'error': 'invalid image type!'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        cover_image = ContentFile(
            decode_file(cover_image), f'{name}{type_}'
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
        return Response(response, status=201)
