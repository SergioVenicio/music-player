
import json

from django.db import IntegrityError
from django.core.files.base import ContentFile

from rest_framework import viewsets
from rest_framework.response import Response

from ..models import Band, Genre
from .serializer import BandSerializer, GenreSerializer

from shared.file.services.FileDecoder import FileDecoder


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):
        description = request.data['description']
        genre_image_raw = request.data['genre_image']

        file_decoder = FileDecoder()

        if not genre_image_raw:
            return Response(data={
                'status': 'error',
                'error': 'Genre image field is required!'
            }, status=400)

        try:
            decoded_image = file_decoder.execute(genre_image_raw, description)
        except ValueError as e:
            print(e)
            return Response(data={
                'status': 'error',
                'error': 'Invalid file type!'
            }, status=400)

        genero = Genre(description=description, genre_image=decoded_image)
        try:
            genero.save()
            return Response(data=json.dumps({
                'genre': {
                    'id': genero.id,
                    'description': genero.description,
                    'genre_image': genero.genre_image.path
                }
            }), status=201)
        except IntegrityError:
            return Response(data={
                'status': 'error',
                'error': 'Invalid genre description!'
            }, status=400)


class BandViewSet(viewsets.ModelViewSet):
    queryset = Band.objects.all()
    serializer_class = BandSerializer
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
