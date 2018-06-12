from music_player.api import viewset
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)
router.register(r'genero', viewset.GeneroViewSet, base_name='genero')
router.register(r'banda', viewset.BandaViewSet, base_name='banda')
router.register(r'album', viewset.AlbumViewSet, base_name='album')
router.register(r'musicas', viewset.MusicaViewSet, base_name='musica')
router.register(
    r'musicas/album/(?P<album_id>.+)', viewset.MusicaViewSet,
    base_name='musica_filter'
)
