"""
    Views básicas do projeto, music-player
"""

from . import forms
from music_player import settings
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from music_player.core.utils import get_all_musics, get_albuns


def home(request):
    """ Retorna todos os albuns cadastrados no sistema """

    page = request.GET.get('page', 1)
    if not page:
        page = 1

    per_page = request.GET.get('per_page', None)
    if per_page is None or per_page == '':
        per_page = settings.PERPAGE
    albuns = get_albuns(per_page=per_page, page=page, pagination=True)

    context = {
        'albuns': albuns,
        'page': albuns.number,
        'per_page': per_page,
        'total_pages': albuns.paginator.num_pages
    }
    return render(request, 'core/home.html', context)


def musicas(request, album_id):
    """ Retorna as músicas cadastradas no sistema com base no album """
    context = {
        'musics': get_all_musics(album_id=album_id),
        'album': get_albuns(album_id=album_id)
    }
    return render(request, 'core/musicas.html', context)


def add_musicas(request):
    """ Adiciona musicas no banco de dados """
    if request.method == 'GET':
        form = forms.MusicaForm()
        context = {
            'form': form
        }
        return render(request, 'core/add_music.html', context=context)
    else:
        raise PermissionDenied()
