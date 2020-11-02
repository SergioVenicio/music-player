import base64
from django.core.paginator import Paginator, EmptyPage

from music_player import settings

from album.models import Album
from band.models import Band, Genre
from music.models import Music


def get_generos(genero_id=None, per_page=None, page=1, pagination=False):
    if genero_id is None:
        generos = Genre.objects.all()
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
        return Genre.objects.get(pk=genero_id)


def get_bandas(banda_id=None, genero_id=None, per_page=None,
               page=1, pagination=False):
    if banda_id is None:
        bandas = Band.objects.all()
        if genero_id is not None:
            bandas = bandas.filter(genre_id=genero_id)

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
        return Band.objects.get(pk=banda_id)


def get_albuns(album_id=None, banda_id=None, per_page=None,
               page=1, pagination=False):
    if album_id is None:
        albuns = Album.objects.all()
        if banda_id is not None:
            albuns = albuns.filter(band_id=banda_id)

        albuns = albuns.order_by('release_date')

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
        return Album.objects.get(pk=album_id)


def get_all_musics(album_id=None):
    if album_id is None:
        return Music.objects.all()

    return Music.objects.filter(album_id=album_id)


def get_file_type(base64_data, musica=False, imagen=True):
    data_type = base64_data[:10]
    if musica:
        if data_type == 'data:audio':
            audio_type = base64_data[11:15]
            if audio_type == 'mpeg' or audio_type == 'mp3;':
                return '.mp3'
            else:
                return False
        else:
            return False
    elif imagen:
        if data_type == 'data:image':
            if base64_data[11:14] == 'png':
                return 'png'
            elif base64_data[11:15] == 'jpeg':
                return 'jpg'
            else:
                return False
        else:
            return False

    return False
