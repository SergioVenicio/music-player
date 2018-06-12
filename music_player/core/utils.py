import base64
import hashlib
from music_player import settings
from music_player.core import models
from django.core.paginator import Paginator, EmptyPage


def get_generos(genero_id=None, per_page=None, page=1, pagination=False):
    if genero_id is None:
        generos = models.Genero.objects.all()
        if pagination:
            if not per_page:

                per_page = settings.PERPAGE
            paginator = Paginator(generos, per_page)
            try:
                return paginator.page(page)
            except EmptyPage:
                return paginator.page(paginator.num_pages)
        else:
            return generos
    else:
        return models.Genero.objects.get(pk=genero_id)


def get_bandas(banda_id=None, genero_id=None, per_page=None,
               page=1, pagination=False):
    if banda_id is None:
        bandas = models.Banda.objects.all()
        if genero_id is not None:
            bandas = bandas.filter(genero_id=genero_id)

        if pagination:
            if not per_page:

                per_page = settings.PERPAGE
            paginator = Paginator(bandas, per_page)
            try:
                return paginator.page(page)
            except EmptyPage:
                return paginator.page(paginator.num_pages)
        else:
            return bandas
    else:
        return models.Banda.objects.get(pk=banda_id)


def get_albuns(album_id=None, banda_id=None, per_page=None,
               page=1, pagination=False):
    if album_id is None:
        albuns = models.Album.objects.all()
        if banda_id is not None:
            albuns = albuns.filter(banda_id=banda_id)

        if pagination:
            if not per_page:

                per_page = settings.PERPAGE
            paginator = Paginator(albuns, per_page)
            try:
                return paginator.page(page)
            except EmptyPage:
                return paginator.page(paginator.num_pages)
        else:
            return albuns
    else:
        return models.Album.objects.get(pk=album_id)


def get_all_musics(album_id=None):
    if album_id is None:
        return models.Musica.objects.all()

    return models.Musica.objects.filter(album_id=album_id)


def get_file_type(base64_data, musica=False, imagen=True):
    data_type = base64_data[:10]
    if musica:
        if data_type == 'data:audio':
            if base64_data[11:15] == 'mpeg':
                return '.mp3'
            else:
                return False
        else:
            return False
    elif imagen:
        print(base64_data[11:15])
        if data_type == 'data:image':
            if base64_data[11:14] == 'png':
                return '.png'
            elif base64_data[11:15] == 'jpeg':
                return '.jpg'
            else:
                return False
        else:
            return False

    return False


def decode_file(base64_data):
    return base64.b64decode(base64_data)


def get_etag(request, id):
    return hashlib.sha1(f"{id}".encode('utf-8')).hexdigest()
