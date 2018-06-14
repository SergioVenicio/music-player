from music_player.api import viewset
from django.urls import include, path
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


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_auth.urls')),
]
