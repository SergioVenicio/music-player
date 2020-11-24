import json
from rest_framework import viewsets
from rest_framework.response import Response

from ..models import Music
from .serializer import MusicSerializer

from dependency_injector.wiring import inject, Provide

from music_player.containers import Container
from shared.file.services.FileDecoder import FileDecoder
from shared.cache.services.CacheService import CacheService


class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer
    http_method_names = ['get', 'post']

    @inject
    def get_queryset(
        self,
        cache: CacheService = Provide[Container.cache_service]
    ):
        cache_key = 'musics'
        album_id = self.request.query_params.get('album_id')

        if album_id is not None:
            cache_key = f'musics@{album_id}'

        data = cache.get(cache_key)
        if data is None:
            if album_id is None:
                queryset = Music.objects.all()
            else:
                queryset = Music.objects.filter(
                    album_id=album_id
                )

            data = [
                music.to_dict()
                for music in queryset
            ]

            cache.set(
                cache_key,
                data
            )

        return data

    @inject
    def retrieve(
        self,
        request,
        pk=None,
        cache: CacheService = Provide[Container.cache_service]
    ):
        cache_key = f'music@{pk}'
        cache_data = cache.get(cache_key)
        if cache_data:
            return Response(cache_data)

        def filter_id(music: dict):
            music_id = music.get(('id'))
            return music_id is not None and str(music_id) == str(pk)

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
            file_decoder: FileDecoder = Provide[Container.file_decoder_service],
    ):
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
