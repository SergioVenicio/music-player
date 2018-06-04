import base64
from music_player import settings
from core.models import Musica, Album
from django.core.paginator import Paginator, EmptyPage


def get_albuns(album_id=None, per_page=None, page=1, pagination=False):
    if album_id is None:
        albuns = Album.objects.all()
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

    return Album.objects.get(pk=album_id)


def get_all_musics(album_id=None):
    if album_id is None:
        return Musica.objects.all()

    return Musica.objects.filter(album_id=album_id)


def get_file_type(base64_data):
    data_type = base64_data[:10]
    if data_type == 'data:audio':
        if base64_data[11:15] == 'mpeg':
            return '.mp3'
    else:
        return False


def decode_file(base64_data):
    return base64.b64decode(base64_data)
