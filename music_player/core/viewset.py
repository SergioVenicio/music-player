import json
from rest_framework import viewsets
from django.http import JsonResponse
from django.db import IntegrityError
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
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        erros = []
        descricao = request.data['descricao']

        try:
            imagem = request.data['imagem']
            tipo = get_file_type(imagem)
        except KeyError:
            genero = Genero(descricao=descricao)
            try:
                genero.save()
            except IntegrityError:
                erros.append('Já existe um genero com essa descrição')
            else:
                response = json.dumps({
                    'genero': {
                        'id': genero.id,
                        'descricao': genero.descricao
                    }
                })
                return JsonResponse(response, safe=False, status=201)
        else:
            if tipo:
                if tipo == '.jpg':
                    imagem = imagem[23:]
                elif tipo == '.png':
                    imagem = imagem[22:]
                imagem = ContentFile(
                    decode_file(imagem), (descricao + tipo)
                )
                genero = Genero(descricao=descricao, imagem=imagem)
                try:
                    genero.save()
                except IntegrityError:
                    erros.append('Já existe um genero com essa descrição')
                else:
                    response = json.dumps({
                        'genero': {
                            'id': genero.id,
                            'descricao': genero.descricao,
                            'imagem': genero.imagem.path
                        }
                    })
                    return JsonResponse(response, safe=False, status=201)
            else:
                erros.append('Tipo de arquivo inválido')

        return JsonResponse(
            json.dumps({'erros': erros}), safe=False, status=400
        )


class BandaViewSet(viewsets.ModelViewSet):
    """
    Endpoint para as bandas
    """

    queryset = Banda.objects.all()
    serializer_class = serializers.BandaSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        erros = []
        nome = request.data.get('nome', None)
        genero_id = request.data.get('genero_id', None)
        imagem = request.data.get('imagem', None)

        if imagem:
            tipo = get_file_type(imagem)
            if tipo:
                if tipo == '.jpg':
                    imagem = imagem[23:]
                elif tipo == '.png':
                    imagem = imagem[22:]
                imagem = ContentFile(
                    decode_file(imagem), (nome + tipo)
                )
                if genero_id:
                    banda = Banda(
                        nome=nome, genero_id=genero_id, imagem=imagem
                    )
                    try:
                        banda.save()
                    except IntegrityError:
                        erros.append('Já existe uma banda com esse nome')
                    else:
                        response = json.dumps({
                            'genero': {
                                'id': banda.id,
                                'nome': banda.nome,
                                'imagem': banda.imagem.path
                            }
                        })
                        return JsonResponse(response, safe=False, status=201)
                else:
                    erros.append('O campo genero é obrigátorio')
            else:
                erros.append('Tipo de arquivo inválido')
        else:
            if genero_id:
                banda = Banda(nome=nome, genero_id=genero_id)
                try:
                    banda.save()
                except IntegrityError:
                    erros.append('Já existe uma banda com esse nome')
                else:
                    response = json.dumps({
                        'genero': {
                            'id': banda.id,
                            'nome': banda.nome,
                            'genero_id': genero_id
                        }
                    })
                    return JsonResponse(response, safe=False, status=201)
            else:
                erros.append('O campo genero é obrigátorio')

        return JsonResponse(
            json.dumps({'erros': erros}), safe=False, status=400
        )


class AlbumViewSet(viewsets.ModelViewSet):
    """
    Endpoint para os albums.
    """

    queryset = Album.objects.all()
    serializer_class = serializers.AlbumSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        erros = []
        nome = request.data.get('nome', None)
        banda_id = request.data.get('banda_id', None)
        data_lancamento = request.data.get('data_lancamento', None)
        imagem = request.data.get('capa', None)

        if not data_lancamento:
            erros.append('O campo data de lançamento é obrigatório')

        if imagem:
            tipo = get_file_type(imagem)
            if tipo:
                if tipo == '.jpg':
                    imagem = imagem[23:]
                elif tipo == '.png':
                    imagem = imagem[22:]
                imagem = ContentFile(
                    decode_file(imagem), (nome + tipo)
                )
                if banda_id:
                    album = Album(
                        nome=nome, banda_id=banda_id,
                        data_lancamento=data_lancamento, capa=imagem
                    )
                    try:
                        album.save()
                    except IntegrityError:
                        erros.append('Já existe um album com esse nome')
                    else:
                        response = json.dumps({
                            'album': {
                                'id': album.id,
                                'nome': album.nome,
                                'banda_id': album.banda.id,
                                'data_lancamento': album.data_lancamento,
                                'capa': album.capa.path
                            }
                        })
                        return JsonResponse(response, safe=False, status=201)
                else:
                    erros.append('O campo banda é obrigátorio')
            else:
                erros.append('Tipo de arquivo inválido')
        else:
            if nome and banda_id:
                album = Album(
                    nome=nome, banda_id=banda_id,
                    data_lancamento=data_lancamento
                )
                try:
                    album.save()
                except IntegrityError:
                    erros.append('Já existe um album com esse nome')
                else:
                    response = json.dumps({
                        'album': {
                            'id': album.id,
                            'nome': album.nome,
                            'banda_id': album.banda.id,
                            'data_lancamento': album.data_lancamento
                        }
                    })
                    return JsonResponse(response, safe=False, status=201)
            else:
                if not nome:
                    erros.append('O campo nome é obrigátorio')
                if not banda_id:
                    erros.append('O campo banda é obrigátorio')

        return JsonResponse(
            json.dumps({'erros': erros}), safe=False, status=400
        )


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
        erros = []
        nome = request.data.get('nome', None)
        album = request.data.get('album', None)
        ordem = request.data.get('ordem', None)
        arquivo = request.data.get('arquivo', None)
        if arquivo:
            tipo = get_file_type(arquivo, musica=True)
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
                if existe:
                    erros.append('Já existe uma música com essa ordem')
                if not tipo:
                    erros.append('Tipo de arquivo inválido')
        else:
            erros.append('O arquivo de música é obrigatório')
        response = json.dumps({'erros': erros})
        return JsonResponse(response, safe=False, status=400)
