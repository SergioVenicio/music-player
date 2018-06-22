import json
from . import serializers
from django.http import Http404
from rest_framework import viewsets
from music_player.core import models
from django.http import JsonResponse
from django.db import IntegrityError
from django.core.files.base import ContentFile
from music_player.core.utils import get_file_type, decode_file


class GeneroViewSet(viewsets.ModelViewSet):
    """
    Endpoint para os generos músicais
    """
    queryset = models.Genero.objects.all()
    serializer_class = serializers.GeneroSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        erros = []
        descricao = request.data['descricao']

        try:
            imagem = request.data['imagem']
            tipo = get_file_type(imagem)
        except KeyError:
            genero = models.Genero(descricao=descricao)
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
                genero = models.Genero(descricao=descricao, imagem=imagem)
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

    queryset = models.Banda.objects.all()
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
                    banda = models.Banda(
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
                banda = models.Banda(nome=nome, genero_id=genero_id)
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

    queryset = models.Album.objects.all()
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
                    album = models.Album(
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
                album = models.Album(
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

    queryset = models.Musica.objects.all()
    serializer_class = serializers.MusicaSerializer
    http_method_names = ['get', 'post']

    def get_queryset(self):
        self.serializer_class = serializers.MusicaSerializerList
        try:
            musicas = models.Musica.objects.filter(
                album_id=self.kwargs['album_id']
            )
        except KeyError:
            musicas = models.Musica.objects.all()
        return musicas

    def create(self, request, *args, **kwargs):
        erros = []
        nome = request.data.get('nome', None)
        album = request.data.get('album', None)
        ordem = request.data.get('ordem', None)
        if not ordem:
            erros.append('O campo ordem é obrigatório')

        if not album:
            erros.append('O campo ordem é obrigatório')

        arquivo = request.data.get('arquivo', None)
        if arquivo:
            tipo = get_file_type(arquivo, musica=True)
            try:
                existe = models.Musica.objects.get(ordem=ordem, album_id=album)
            except models.Musica.DoesNotExist:
                existe = False
            except ValueError:
                existe = False

            if not existe and tipo:
                arquivo = ContentFile(
                    decode_file(arquivo), (nome + tipo)
                )

                try:
                    musica = models.Musica(
                        nome=nome, album_id=album, ordem=ordem, arquivo=arquivo
                    )
                    musica.save()
                except Exception:
                    pass
                else:
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


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = models.Usuario.objects.all()
    serializer_class = serializers.UsuarioSerializer
    http_method_names = ['get']


class LikesViewSet(viewsets.ModelViewSet):
    queryset = models.Like.objects.all()
    serializer_class = serializers.LikeSerializer
    http_method_names = ['get', 'post', 'delete', 'head']

    def get_queryset(self):
        likes = models.Like.objects.all()

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
                likes = likes.filter(usuario_id=usuario_id)
            except ValueError:
                raise Http404('Conteudo não encontrado')

        if musica_id:
            try:
                likes = likes.filter(musica_id=musica_id)
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
            existe = models.Like.objects.get(
                usuario_id=usuario_id, musica_id=musica_id
            )
        except models.Like.DoesNotExist:
            existe = False

        if existe:
            response = json.dumps({
                'like': {
                    'id': existe.id,
                    'usuario': existe.usuario.id,
                    'musica': existe.musica.id,
                    'data': str(existe.data)
                }
            })
            status = 201

        if not erros and not existe:
            like = models.Like(usuario_id=usuario_id, musica_id=musica_id)
            like.save()
            response = json.dumps({
                'like': {
                    'id': like.id,
                    'usuario': like.usuario.id,
                    'musica': like.musica.id,
                    'data': str(like.data)
                }
            })
            status = 201
        elif erros and not existe:
            response = json.dumps({'erros': erros})
            status = 400

        return JsonResponse(response, safe=False, status=status)
