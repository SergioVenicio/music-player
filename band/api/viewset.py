
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
        except ValueError:
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
        file_decoder = FileDecoder()

        name = request.data.get('name', None)
        genre_id = request.data.get('genre_id', None)
        band_image_raw = request.data.get('band_image', None)

        if not name:
            return Response(data={
                'status': 'error',
                'error': 'Band name fild is required!'
            }, status=400)

        if not genre_id:
            return Response(data={
                'status': 'error',
                'error': 'Genre id fild is required!'
            }, status=400)

        if not band_image_raw:
            return Response(data={
                'status': 'error',
                'error': 'Band image fild is required!'
            }, status=400)

        try:
            band_image = file_decoder.execute(band_image_raw, name)
        except ValueError:
            return Response(data={
                'status': 'error',
                'error': 'Invalid image type!'
            }, status=400)

        band = Band(
            name=name,
            genre_id=genre_id,
            band_image=band_image
        )
        try:
            band.save()
        except IntegrityError:
            return Response(data={
                'status': 'error',
                'error': 'This band already exists!'
            }, status=400)

        return Response(data={
            'band': {
                'id': band.id,
                'name': band.name,
                'band_image': band.band_image.path
            }
        }, status=201)
