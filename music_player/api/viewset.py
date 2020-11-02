import json
from . import serializers
from django.http import Http404
from rest_framework import viewsets
from django.db import IntegrityError
from rest_framework.response import Response
from django.core.files.base import ContentFile

from band.models import Band, Genre
from music.models import Music
from album.models import Album
from user.models import User, Like

from music_player.core.utils import get_file_type, decode_file


class GeneroViewSet(viewsets.ModelViewSet):
    """
    Endpoint para os generos músicais
    """
    queryset = Genre.objects.all()
    serializer_class = serializers.GeneroSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        erros = []
        description = request.data['description']

        imagem = request.data['genre_image']
        tipo = get_file_type(imagem)
        if tipo:
            if tipo == '.jpg':
                imagem = imagem[23:]
            elif tipo == '.png':
                imagem = imagem[22:]
            imagem = ContentFile(
                decode_file(imagem), (description + tipo)
            )
            print(imagem)
            genero = Genre(description=description, genre_image=imagem)
            try:
                genero.save()
            except IntegrityError:
                erros.append('Já existe um genero com essa descrição')
            else:
                response = json.dumps({
                    'genero': {
                        'id': genero.id,
                        'descricao': genero.description,
                        'imagem': genero.genre_image.path
                    }
                })
                return Response(response, status=201)
        else:
            erros.append('Tipo de arquivo inválido')

        return Response(
            json.dumps({'erros': erros}), status=400
        )


class BandaViewSet(viewsets.ModelViewSet):
    """
    Endpoint para as bandas
    """

    queryset = Band.objects.all()
    serializer_class = serializers.BandaSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        erros = []
        nome = request.data.get('name', None)
        genero_id = request.data.get('genre_id', None)
        imagem = request.data.get('band_image', None)

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
                    banda = Band(
                        name=nome,
                        genre_id=genero_id,
                        band_image=imagem
                    )
                    try:
                        banda.save()
                    except IntegrityError:
                        erros.append('Já existe uma banda com esse nome')
                    else:
                        response = json.dumps({
                            'genero': {
                                'id': banda.id,
                                'nome': banda.name,
                                'imagem': banda.band_image.path
                            }
                        })
                        return Response(response, status=201)
                else:
                    erros.append('O campo genero é obrigátorio')
            else:
                erros.append('Tipo de arquivo inválido')
        else:
            if genero_id:
                banda = Band(name=nome, genre_id=genero_id)
                try:
                    banda.save()
                except IntegrityError:
                    erros.append('Já existe uma banda com esse nome')
                else:
                    response = json.dumps({
                        'genero': {
                            'id': banda.id,
                            'nome': banda.name,
                            'genero_id': genero_id
                        }
                    })
                    return Response(response, status=201)
            else:
                erros.append('O campo genero é obrigátorio')

        return Response(
            json.dumps({'erros': erros}), status=400
        )


class AlbumViewSet(viewsets.ModelViewSet):
    """
    Endpoint para os albums.
    """

    queryset = Album.objects.all().order_by('data_lancamento')
    serializer_class = serializers.AlbumSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        erros = []
        nome = request.data.get('name', None)
        banda_id = request.data.get('band_id', None)
        data_lancamento = request.data.get('release_date', None)
        imagem = request.data.get('cover_image', None)

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
                        name=nome,
                        band_id=banda_id,
                        release_date=data_lancamento,
                        cover_image=imagem
                    )
                    album.save()
                    response = json.dumps({
                        'album': {
                            'id': album.id,
                            'nome': album.name,
                            'banda_id': album.band.id,
                            'data_lancamento': album.release_date,
                            'capa': album.cover_image.path
                        }
                    })
                    return Response(response, status=201)
                else:
                    erros.append('O campo banda é obrigátorio')
            else:
                erros.append('Tipo de arquivo inválido')
        else:
            if nome and banda_id and data_lancamento:
                album = Album(
                    name=nome,
                    band_id=banda_id,
                    release_date=data_lancamento
                )
                album.save()
                response = json.dumps({
                    'album': {
                        'id': album.id,
                        'nome': album.name,
                        'banda_id': album.band.id,
                        'data_lancamento': album.release_date
                    }
                })
                return Response(response, status=201)
            else:
                if not nome:
                    erros.append('O campo nome é obrigátorio')
                if not banda_id:
                    erros.append('O campo banda é obrigátorio')
                if not data_lancamento:
                    erros.append('O campo data de lançamento é obrigátorio')

        return Response(
            json.dumps({'erros': erros}), status=400
        )


class MusicaViewSet(viewsets.ModelViewSet):
    """
    EndPoint para as músicas.

    """

    queryset = Music.objects.all()
    serializer_class = serializers.MusicaSerializer
    http_method_names = ['get', 'post']

    def get_queryset(self):
        self.serializer_class = serializers.MusicaSerializerList
        try:
            musicas = Music.objects.filter(
                album_id=self.kwargs['album_id']
            )
        except KeyError:
            musicas = Music.objects.all()
        return musicas

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


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UsuarioSerializer
    http_method_names = ['get']


class LikesViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = serializers.LikeSerializer
    http_method_names = ['get', 'post', 'delete', 'head']

    def get_queryset(self):
        likes = Like.objects.all()

        try:
            usuario_id = self.kwargs['usuario_id']
        except KeyError:
            usuario_id = None

        try:
            musica_id = self.kwargs['musica_id']
        except KeyError:
            musica_id = None

        if usuario_id is not None and musica_id is None:
            self.serializer_class = serializers.LikeSerializerMusica
        elif usuario_id is not None or musica_id is not None:
            self.serializer_class = serializers.LikeSerializerUsuario

        if usuario_id:
            try:
                likes = likes.filter(user_id=usuario_id)
            except ValueError:
                raise Http404('Conteudo não encontrado')

        if musica_id:
            try:
                likes = likes.filter(music_id=musica_id)
            except ValueError:
                raise Http404('Conteudo não encontrado')

        return likes

    def create(self, request, *args, **kwargs):
        erros = []
        usuario_id = request.data.get('usuario', None)
        musica_id = request.data.get('musica', None)

        if not usuario_id:
            erros.append('O campo usuário é obrigatório')
        if not musica_id:
            erros.append('O campo música é obrigatório')

        try:
            existe = Like.objects.get(
                user_id=usuario_id, music_id=musica_id
            )
        except Like.DoesNotExist:
            existe = False

        if existe:
            response = json.dumps({
                'like': {
                    'id': existe.id,
                    'user': existe.user.id,
                    'music': existe.music.id,
                    'date': str(existe.date)
                }
            })
            status = 201

        if not erros and not existe:
            like = Like(user_id=usuario_id, music_id=musica_id)
            like.save()
            response = json.dumps({
                'like': {
                    'id': like.id,
                    'user': like.user.id,
                    'music': like.music.id,
                    'date': str(like.date)
                }
            })
            status = 201
        elif erros and not existe:
            response = json.dumps({'erros': erros})
            status = 400

        return Response(response, status=status)
