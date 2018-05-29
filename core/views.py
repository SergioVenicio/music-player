"""
    Views básicas do projeto, music-player
"""

from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from .utils import get_all_musics, get_albuns
from . import forms


def home(request):
    """ Retorna todos os albuns cadastrados no sistema """
    context = {
        'albuns': get_albuns()
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
