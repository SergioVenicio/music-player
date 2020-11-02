from . import utils
from music_player import settings
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


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
    from band.forms import BandForm
    form = BandForm()
    context = {'form': form}
    return render(request, 'core/add_bandas.html', context)


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
    from album.forms import AlbumForm
    form = AlbumForm()
    context = {'form': form}
    return render(request, 'core/add_albuns.html', context)


@login_required(login_url='/login')
def musicas(request, id):
    context = {
        'musics': utils.get_all_musics(album_id=id),
        'album': utils.get_albuns(album_id=id)
    }
    return render(request, 'core/musicas.html', context)


@login_required(login_url='/login')
def favoritas(request):
    return render(request, 'core/favoritas.html')


@login_required(login_url='/login')
def add_musicas(request):
    from music.forms import MusicForm

    if request.method == 'GET':
        form = MusicForm()
        context = {
            'form': form
        }
        return render(request, 'core/add_music.html', context=context)
    else:
        raise PermissionDenied()


@login_required(login_url='/login')
def add_generos(request):
    from band.forms import GernreForm
    if request.method == 'GET':
        form = GernreForm()
        context = {
            'form': form
        }
        return render(request, 'core/add_generos.html', context)
    else:
        raise PermissionDenied()
