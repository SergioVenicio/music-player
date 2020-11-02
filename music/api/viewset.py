import json
from rest_framework import viewsets
from rest_framework.response import Response
from django.core.files.base import ContentFile

from ..models import Music
from .serializer import MusicSerializer, MusicSerializerList

from music_player.core.utils import get_file_type, decode_file


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
        erros = []
        nome = request.data.get('name', None)
        album = request.data.get('album', None)
        ordem = request.data.get('order', None)

        if not ordem:
            erros.append('O campo ordem é obrigatório')

        if not album:
            erros.append('O campo album é obrigatório')

        arquivo = request.data.get('file', None)
        if arquivo:
            tipo = get_file_type(arquivo, musica=True)
            if not erros:
                try:
                    existe = Music.objects.get(
                        order=ordem,
                        album_id=album
                    )
                except Music.DoesNotExist:
                    existe = False
            else:
                existe = False

            if not existe and tipo and ordem and not erros:
                arquivo = arquivo.replace('data:audio/mp3;base64,', '')
                arquivo = arquivo.replace('data:audio/mpeg;base64,', '')
                arquivo = ContentFile(decode_file(arquivo), (nome + tipo))

                musica = Music(
                    name=nome,
                    album_id=album,
                    order=ordem,
                    file=arquivo
                )
                musica.save()
                response = json.dumps({
                    'musica': {
                        'id': musica.id,
                        'nome': musica.name,
                        'ordem': musica.order,
                        'tipo': musica.file_type,
                        'arquivo': musica.file.path
                    }
                })
                return Response(response, status=201)
            else:
                if existe:
                    erros.append('Já existe uma música com essa ordem')
                if not tipo:
                    erros.append('Tipo de arquivo inválido')
                if not ordem:
                    erros.append('Ordem inválida')
        else:
            erros.append('O arquivo de música é obrigatório')
        response = json.dumps({'erros': erros})
        return Response(response, status=400)
