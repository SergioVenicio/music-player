import json
from rest_framework import viewsets
from django.http import JsonResponse
from music_player.core import serializers
from django.core.files.base import ContentFile
from music_player.core.utils import get_file_type, decode_file
from music_player.core.models import Genero, Banda, Album, Musica


class GeneroViewSet(viewsets.ModelViewSet):
    """
    Endpoint para os generos músicais
    """
    queryset = Genero.objects.all()
    serializer_class = serializers.GeneroSerializer
    http_method_names = ['get']


class BandaViewSet(viewsets.ModelViewSet):
    """
    Endpoint para as bandas
    """

    queryset = Banda.objects.all()
    serializer_class = serializers.BandaSerializer
    http_method_names = ['get']


class AlbumViewSet(viewsets.ModelViewSet):
    """
    Endpoint para os albums.
    """

    queryset = Album.objects.all()
    serializer_class = serializers.AlbumSerializer
    http_method_names = ['get']


class MusicaViewSet(viewsets.ModelViewSet):
    """
    EndPoint para as músicas.

    """

    queryset = Musica.objects.all()
    serializer_class = serializers.MusicaSerializer
    http_method_names = ['get', 'post']

    def get_queryset(self):
        self.serializer_class = serializers.MusicaSerializerList
        try:
            musicas = Musica.objects.filter(album_id=self.kwargs['album_id'])
        except KeyError:
            musicas = Musica.objects.all()
        return musicas

    def create(self, request, *args, **kwargs):
        nome = request.data['nome']
        album = request.data['album']
        ordem = request.data['ordem']
        arquivo = request.data['arquivo']
        tipo = get_file_type(arquivo)
        try:
            existe = Musica.objects.get(ordem=ordem, album_id=album)
        except Musica.DoesNotExist:
            existe = False

        if not existe and tipo:
            arquivo = ContentFile(
                decode_file(arquivo), (nome + tipo)
            )
            musica = Musica(
                nome=nome, album_id=album, ordem=ordem, arquivo=arquivo
            )
            musica.save()
            response = json.dumps({
                'musica': {
                    'id': musica.id,
                    'nome': musica.nome,
                    'ordem': musica.ordem,
                    'tipo': musica.arquivo_tipo,
                    'arquivo': musica.arquivo.path
                }
            })
            return JsonResponse(response, safe=False, status=201)
        else:
            erros = []
            if existe:
                erros.append('Já existe uma música com essa ordem')
            if not tipo:
                erros.append('Tipo de arquivo inválido')

            response = json.dumps({'erros': erros})
            return JsonResponse(response, safe=False, status=400)
