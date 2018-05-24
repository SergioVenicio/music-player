import base64
from core.models import Musica, Album


def get_albuns(album_id=None):
    if album_id is None:
        return Album.objects.all()

    return Album.objects.get(pk=album_id)


def get_all_musics(album_id=None):
    if album_id is None:
        return Musica.objects.all()

    return Musica.objects.filter(album_id=album_id).order_by('ordem')


def get_file_type(base64_data):
    data_type = base64_data[:10]
    extenxion = base64_data[11:15]
    if data_type == 'data:audio':
        if extenxion == 'mpeg':
            return '.mp3'
    else:
        return False


def decode_file(base64_data):
    return base64.b64decode(base64_data)
