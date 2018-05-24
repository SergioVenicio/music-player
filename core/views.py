from . import forms
from .utils import get_all_musics, get_albuns
from django.shortcuts import render


def home(request):
    context = {
        'albuns': get_albuns()
    }
    return render(request, 'core/home.html', context)


def musicas(request, album_id):
    context = {
        'musics': get_all_musics(album_id=album_id),
        'album': get_albuns(album_id=album_id)
    }
    return render(request, 'core/musicas.html', context)


def add_musicas(request):
    if request.method == 'GET':
        form = forms.MusicaForm()
        context = {
            'form': form
        }
        return render(request, 'core/add_music.html', context=context)
