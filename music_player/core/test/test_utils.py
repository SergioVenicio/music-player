import pytest
from music_player.core import utils


@pytest.mark.django_db(transaction=True)
def test_get_generos(genero):
    db_genero = utils.get_generos()
    assert genero in db_genero


@pytest.mark.django_db(transaction=True)
def test_get_generos_id(genero):
    db_genero = utils.get_generos(genero_id=genero.id)
    assert genero.id == db_genero.id


@pytest.mark.django_db(transaction=True)
def test_get_generos_pagination(genero):
    db_genero = utils.get_generos(pagination=True)
    assert db_genero.number == 1


@pytest.mark.django_db(transaction=True)
def test_get_generos_pagination_empty(genero):
    db_genero = utils.get_generos(page=10, pagination=True)
    assert db_genero.number == 1


@pytest.mark.django_db(transaction=True)
def test_get_banda(banda):
    db_banda = utils.get_bandas()
    assert banda in db_banda


@pytest.mark.django_db(transaction=True)
def test_get_banda_id(banda):
    db_banda = utils.get_bandas(banda_id=banda.id)
    assert banda.id == db_banda.id


@pytest.mark.django_db(transaction=True)
def test_get_banda_genero_id(banda, genero):
    db_banda = utils.get_bandas(genero_id=genero.id)
    assert db_banda[0].genero.id == genero.id


@pytest.mark.django_db(transaction=True)
def test_get_banda_pagination(banda):
    db_banda = utils.get_bandas(pagination=True)
    assert db_banda.number == 1


@pytest.mark.django_db(transaction=True)
def test_get_banda_pagination_empty(banda):
    db_banda = utils.get_bandas(page=10, pagination=True)
    assert db_banda.number == 1


@pytest.mark.django_db(transaction=True)
def test_get_album(album):
    db_album = utils.get_albuns()
    assert album in db_album


@pytest.mark.django_db(transaction=True)
def test_get_album_id(album):
    db_album = utils.get_albuns(album_id=album.id)
    assert album.id == db_album.id


@pytest.mark.django_db(transaction=True)
def test_get_album_banda_id(album, banda):
    db_album = utils.get_albuns(banda_id=banda.id)
    assert db_album[0].banda.id == banda.id


@pytest.mark.django_db(transaction=True)
def test_get_album_pagination(album):
    db_album = utils.get_albuns(pagination=True)
    assert db_album.number == 1


@pytest.mark.django_db(transaction=True)
def test_get_album_pagination_empty(album):
    db_album = utils.get_albuns(page=10, pagination=True)
    assert db_album.number == 1


@pytest.mark.django_db(transaction=True)
def test_get_musica(musica):
    db_musica = utils.get_all_musics()
    assert musica in db_musica


@pytest.mark.django_db(transaction=True)
def test_get_musica_album_id(musica, album):
    db_musica = utils.get_all_musics(album_id=album.id)
    assert db_musica[0].album.id == album.id


@pytest.mark.django_db(transaction=True)
def test_get_file_type_mp3(b64_arquivo):
    assert utils.get_file_type(b64_arquivo, musica=True) == '.mp3'


@pytest.mark.django_db(transaction=True)
def test_get_file_type_mp3_error(b64_arquivo_wav):
    assert utils.get_file_type(b64_arquivo_wav, musica=True) is False


@pytest.mark.django_db(transaction=True)
def test_get_file_type_mp3_with_pgn(b64_capa):
    assert utils.get_file_type(b64_capa, musica=True) is False


@pytest.mark.django_db(transaction=True)
def test_get_file_type_png(b64_capa):
    assert utils.get_file_type(b64_capa) == '.png'


@pytest.mark.django_db(transaction=True)
def test_get_file_type_png_with_mp3(b64_arquivo):
    assert utils.get_file_type(b64_arquivo) is False


@pytest.mark.django_db(transaction=True)
def test_get_file_type_without_options(b64_arquivo):
    assert utils.get_file_type(
        b64_arquivo, musica=False, imagen=False
    ) is False


@pytest.mark.django_db(transaction=True)
def test_get_file_type_jpg(b64_capa_jpg):
    assert utils.get_file_type(b64_capa_jpg) == '.jpg'


@pytest.mark.django_db(transaction=True)
def test_get_file_type_error(b64_capa_error):
    assert utils.get_file_type(b64_capa_error) is False


@pytest.mark.django_db(transaction=True)
def test_decode_file(b64_arquivo):
    assert utils.decode_file(b64_arquivo)


@pytest.mark.django_db(transaction=True)
def test_etag(request, usuario):
    request.user = usuario
    assert utils.get_etag(request, 1)
