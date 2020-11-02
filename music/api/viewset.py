import json
from rest_framework import viewsets
from rest_framework.response import Response

from ..models import Music
from .serializer import MusicSerializer, MusicSerializerList

from shared.file.services.FileDecoder import FileDecoder


class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    http_method_names = ['get', 'post']

    def get_queryset(self):
        self.serializer_class = MusicSerializerList
        album_id = self.request.query_params.get('album_id')

        queryset = Music.objects.all()
        if album_id is None:
            return queryset

        return queryset.filter(album_id=album_id)

    def create(self, request, *args, **kwargs):
        file_decoder = FileDecoder()

        name = request.data.get('name', None)
        album_id = request.data.get('album_id', None)
        ordem = request.data.get('order', None)
        file = request.data.get('file', None)

        if not ordem:
            return Response(data={
                'status': 'error',
                'error': 'The order field is required!'
            }, status=400)

        if not album_id:
            return Response(data={
                'status': 'error',
                'error': 'The album_id field is required!'
            }, status=400)

        if not file:
            return Response(data={
                'status': 'error',
                'error': 'The album_id field is required!'
            }, status=400)

        try:
            decode_file = file_decoder.execute(
                file,
                name
            )
        except ValueError:
            return Response(data={
                'status': 'error',
                'error': 'Invalid file type!'
            }, status=400)

        music = Music(
            name=name,
            album_id=album_id,
            order=ordem,
            file=decode_file
        )
        music.save()

        return Response(data=json.dumps({
            'music': {
                'id': music.id,
                'name': music.name,
                'order': music.order,
                'file_type': music.file_type,
                'file': music.file.path
            }
        }), status=201)
