import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets

from ..models import Album
from .serializer import AlbumSerializer


from shared.file.services.FileDecoder import FileDecoder


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all().order_by('release_date')
    serializer_class = AlbumSerializer
    http_method_names = ['get', 'post']

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
