from music_player.api import viewset
from django.urls import include, path
from rest_framework.routers import DefaultRouter


router = DefaultRouter(trailing_slash=False)
router.register(r'genero', viewset.GeneroViewSet, basename='genero')
router.register(r'banda', viewset.BandaViewSet, basename='banda')
router.register(r'album', viewset.AlbumViewSet, basename='album')
router.register(r'musicas', viewset.MusicaViewSet, basename='musica')
router.register(
    r'musicas/album/(?P<album_id>.+)', viewset.MusicaViewSet,
    basename='musica_filter'
)
router.register(r'usuarios', viewset.UsuarioViewSet, basename='usuario')
router.register(r'likes', viewset.LikesViewSet, basename='like')
router.register(
    r'likes/usuario/(?P<usuario_id>\w+)/(?P<musica_id>\w+)',
    viewset.LikesViewSet, basename='like_filter_music'
)
router.register(
    r'likes/usuario/(?P<usuario_id>.+)',
    viewset.LikesViewSet, basename='like_filter'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_auth.urls')),
]
