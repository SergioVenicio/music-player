"""
    Views básicas do projeto, music-player
"""

from . import forms
from . import utils
from music_player import settings
from django.shortcuts import render, redirect
from django.views.decorators.http import etag
from django.contrib.auth import login, authenticate
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


def sign_up(request):
    if request.method == 'POST':
        form = forms.UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            usuario = authenticate(email=email, password=password)
            login(request, usuario)
            return redirect('home')
    else:
        form = forms.UsuarioForm()
    context = {'form': form}
    return render(request, 'registration/signup.html', context)


@login_required(login_url='/login')
def user_avatar(request):
    usuario = request.user
    if request.method == 'GET':
        form = forms.UsuarioEditAvatar(instance=usuario)
    else:
        form = forms.UsuarioEditAvatar(
            request.POST, request.FILES, instance=usuario
        )
        if form.is_valid():
            form.save()

    context = {
        'form': form,
        'avatar': usuario.avatar
    }
    return render(request, 'registration/avatar.html', context)


@login_required(login_url='/login')
def home(request):
    """ Retorna todos os albuns cadastrados no sistema """

    page = request.GET.get('page', 1)
    if not page:
        page = 1

    per_page = request.GET.get('per_page', None)
    if per_page is None or per_page == '':
        per_page = settings.PERPAGE
    generos = utils.get_generos(per_page=per_page, page=page, pagination=True)

    context = {
        'generos': generos,
        'page': generos.number,
        'per_page': per_page,
        'total_pages': generos.paginator.num_pages
    }
    return render(request, 'core/home.html', context)


@etag(utils.get_etag)
@login_required(login_url='/login')
def bandas(request, id):
    page = request.GET.get('page', 1)
    if not page:
        page = 1

    per_page = request.GET.get('per_page', None)
    if per_page is None or per_page == '':
        per_page = settings.PERPAGE

    bandas = utils.get_bandas(
        genero_id=id, per_page=per_page, page=page, pagination=True
    )

    context = {
        'bandas': bandas,
        'page': bandas.number,
        'per_page': per_page,
        'total_pages': bandas.paginator.num_pages
    }
    return render(request, 'core/bandas.html', context)


@login_required(login_url='/login')
def add_bandas(request):
    form = forms.BandaForm()
    context = {'form': form}
    return render(request, 'core/add_bandas.html', context)


@etag(utils.get_etag)
@login_required(login_url='/login')
def albuns(request, id):
    page = request.GET.get('page', 1)
    if not page:
        page = 1

    per_page = request.GET.get('per_page', None)
    if per_page is None or per_page == '':
        per_page = settings.PERPAGE

    albuns = utils.get_albuns(
        banda_id=id, per_page=per_page, page=page, pagination=True
    )

    context = {
        'albuns': albuns,
        'page': albuns.number,
        'per_page': per_page,
        'total_pages': albuns.paginator.num_pages
    }
    return render(request, 'core/albuns.html', context)


@login_required(login_url='/login')
def add_albuns(request):
    form = forms.AlbumForm()
    context = {'form': form}
    return render(request, 'core/add_albuns.html', context)


# @etag(utils.get_etag)
@login_required(login_url='/login')
def musicas(request, id):
    """ Retorna as músicas cadastradas no sistema com base no album """
    context = {
        'musics': utils.get_all_musics(album_id=id),
        'album': utils.get_albuns(album_id=id)
    }
    return render(request, 'core/musicas.html', context)


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def add_generos(request):
    if request.method == 'GET':
        form = forms.GeneroForm()
        context = {
            'form': form
        }
        return render(request, 'core/add_generos.html', context)
    else:
        raise PermissionDenied()
