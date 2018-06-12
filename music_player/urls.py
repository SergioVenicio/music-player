from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from music_player.core import viewset
from django.conf.urls.static import static
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
    path('', include('music_player.core.urls')),
    path('admin/', admin.site.urls),
    path('api_v1/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
